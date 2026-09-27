import string

import logging

from app.exceptions.custom_exceptions import (
    PromptAlreadyExistsError,
    PromptNotFoundError,
    PromptVariableError,
    PromptVersionNotFoundError
)

from app.schemas import (PromptCreate,
                        PromptMessage,
                        PromptVersion,
                        PromptResponse,
                        PromptTestCase,
                        PromptTestResult,
                        PromptEvaluationResponse)



logger = logging.getLogger(__name__)

class PromptService:
    def __init__(self):
        self._prompts: dict[str, dict[int,PromptVersion]] = {}


    def create_prompt(self, prompt: PromptCreate) -> PromptCreate:
        if prompt.name in self._prompts:
            logger.error("Prompt already exists: name=%s",
                            prompt.name)
            raise PromptAlreadyExistsError(prompt.name)

        version = PromptVersion(
            version=1,
            messages=prompt.messages
        )
        self._prompts[prompt.name] = {
            1: version,
        }

        logger.info("Prompt created: name=%s version=1",prompt.name)

        return PromptResponse(
            name=prompt.name,
            version=1,
            messages=prompt.messages
        )


    def get_prompt(self, name: str) -> PromptResponse:
        if name not in self._prompts:
            logger.warning("Prompt not found: name=%s", name)
            raise PromptNotFoundError(name)

        latest_version = max(self._prompts[name])

        prompt_version = self._prompts[name][latest_version]

        logger.info("Prompt retrieved: name=%s version=%s",
                    name,
                    latest_version)

        return PromptResponse(
            name=name,
            version=latest_version,
            messages=prompt_version.messages
        )


    def create_version(self, name: str, messages: list[PromptMessage]) -> PromptResponse:

        if name not in self._prompts:
            logger.warning("Prompt not found: name=%s", name)
            raise PromptNotFoundError(name)

        latest_version = max(self._prompts[name])
        new_version = latest_version + 1

        version = PromptVersion(
            version=new_version,
            messages=messages
        )

        self._prompts[name][new_version] = version

        logger.info("Prompt verison created: name=%s version=%s",
                    name,
                    new_version)

        return PromptResponse(
            name=name,
            version=new_version,
            messages=messages
        )

    def get_prompt_version(self, name: str, version: int) -> PromptResponse:

        if name not in self._prompts:
            logger.warning("Prompt not found: name=%s", name)
            raise PromptNotFoundError(name)

        if version not in self._prompts[name]:
            logger.warning("Prompt version not found: name=%s version=%s",
                                        name,
                                        version)
            raise PromptVersionNotFoundError(name, version)

        prompt_version = self._prompts[name][version]

        return PromptResponse(
            name=name,
            version=version,
            messages=prompt_version.messages
        )

    def render_prompt(self, name: str, variables : dict[str, str], version: int | None = None) -> list[PromptMessage]:
        if name not in self._prompts:
            logger.warning("Prompt not found: name=%s", name)
            raise PromptNotFoundError(name)

        if version is None:
            version = max(self._prompts[name])

        if version not in self._prompts[name]:
            logger.warning("Prompt version not found: name=%s version=%s",
                            name,
                            version)
            raise PromptVersionNotFoundError(name, version)


        prompt_version = self._prompts[name][version]

        rendered_messages = []

        for message in prompt_version.messages:
            formatter = string.Formatter()

            required_variables = {
            field_name
            for _, field_name, _, _ in formatter.parse(message.content)
            if field_name is not None
    }

            missing_variables = required_variables - variables.keys()

            if missing_variables:
                logger.warning("Prompt rendering failed due to missing variables: name=%s missing%s",
                                name,
                                sorted(missing_variables))
                raise PromptVariableError(
                    name=name,
                    missing_variables=sorted(missing_variables)
                )

            rendered_content = message.content.format(**variables)

            rendered_messages.append(
                PromptMessage(
                    role=message.role,
                    content=rendered_content
                )
            )

        logger.info("Prompt rendered: name=%s version=%s",
                    name,
                    version)

        return rendered_messages


    def evaluate_prompt(self, name: str, test_cases: list[PromptTestCase], version: int | None = None,) -> PromptEvaluationResponse:

        logger.info("Prompt evaluation started: name=%s version=%s tests=%s",
                    name,
                    version,
                    len(test_cases))

        if name not in self._prompts:
            logger.warning("Prompt not found: name=%s", name)
            raise PromptNotFoundError(name)

        if version is None:
            version = max(self._prompts[name])

        if version not in self._prompts[name]:
            logger.warning("Prompt version not found: name=%s version=%s",
                                        name,
                                        version)
            raise PromptVersionNotFoundError(name, version)

        results = []

        for test_case in test_cases:
            actual_messages = self.render_prompt(
                name,
                test_case.variables,
                version,
            )

            passed = actual_messages == test_case.expected_messages

            results.append(
                PromptTestResult(
                    name=test_case.name,
                    passed=passed,
                    actual_messages=actual_messages,
                    expected_messages=test_case.expected_messages,
                )
            )

        passed_tests = sum(
            1 for result in results if result.passed
        )

        failed_tests = len(results) - passed_tests

        logger.info("Prompt evaluation completed: name=%s version=%s passed=%s failed=%s",
                    name,
                    version,
                    passed_tests,
                    failed_tests)

        return PromptEvaluationResponse(
            prompt_name=name,
            version=version,
            total_tests=len(results),
            passed_tests=passed_tests,
            failed_tests=len(results) - passed_tests,
            results=results,
        )


prompt_service = PromptService()