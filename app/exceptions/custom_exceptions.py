class PromptAlreadyExistsError(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Prompt '{name}' already exists.")


class PromptNotFoundError(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Prompt '{name}' was not found.")


class PromptVariableError(Exception):
    def __init__(self, name: str, missing_variables: list[str]):
        self.name = name
        self.missing_variables = missing_variables

        variables = ", ".join(missing_variables)

        super().__init__(f"Missing variables for prompt '{name}': {variables}")


class PromptVersionNotFoundError(Exception):

    def __init__(self, name: str, version: int):
        self.name = name
        self.version = version

        super().__init__(
            f"Version {version} of prompt '{name}' was not found."
        )


class AIProviderError(Exception):
    def __init__(self, message: str , status_code: int = 502):
        self.status_code = status_code
        super().__init__(message)


class PromptGuardrailError(Exception):
    def __init__(self, message: str):
        super().__init__(message)