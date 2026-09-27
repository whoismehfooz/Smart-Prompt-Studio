from app.schemas import (
    PromptCreate,
    PromptMessage,
    PromptTestCase,
)
from app.services.prompt_service import PromptService


def test_prompt_evaluation_passes():
    service = PromptService()

    service.create_prompt(
        PromptCreate(
            name="evaluation_test",
            messages=[
                {
                    "role": "user",
                    "content": "Explain {topic}.",
                }
            ],
        )
    )

    result = service.evaluate_prompt(
        "evaluation_test",
        [
            PromptTestCase(
                name="recursion_test",
                variables={"topic": "recursion"},
                expected_messages=[
                    PromptMessage(
                        role="user",
                        content="Explain recursion.",
                    )
                ],
            )
        ],
    )

    assert result.total_tests == 1
    assert result.passed_tests == 1
    assert result.failed_tests == 0
    assert result.results[0].passed is True


def test_prompt_evaluation_fails_when_output_differs():
    service = PromptService()

    service.create_prompt(
        PromptCreate(
            name="evaluation_test",
            messages=[
                {
                    "role": "user",
                    "content": "Explain {topic}.",
                }
            ],
        )
    )

    result = service.evaluate_prompt(
        "evaluation_test",
        [
            PromptTestCase(
                name="incorrect_expectation",
                variables={"topic": "recursion"},
                expected_messages=[
                    PromptMessage(
                        role="user",
                        content="Explain recursion in detail.",
                    )
                ],
            )
        ],
    )

    assert result.total_tests == 1
    assert result.passed_tests == 0
    assert result.failed_tests == 1
    assert result.results[0].passed is False


def test_prompt_evaluation_specific_version():
    service = PromptService()

    service.create_prompt(
        PromptCreate(
            name="evaluation_test",
            messages=[
                {
                    "role": "user",
                    "content": "Explain {topic}.",
                }
            ],
        )
    )

    service.create_version(
        "evaluation_test",
        [
            PromptMessage(
                role="user",
                content="Explain {topic} in detail.",
            )
        ],
    )

    result = service.evaluate_prompt(
        "evaluation_test",
        [
            PromptTestCase(
                name="version_two_test",
                variables={"topic": "recursion"},
                expected_messages=[
                    PromptMessage(
                        role="user",
                        content="Explain recursion in detail.",
                    )
                ],
            )
        ],
        version=2,
    )

    assert result.version == 2
    assert result.passed_tests == 1
    assert result.failed_tests == 0