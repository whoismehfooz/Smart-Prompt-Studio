from pydantic import BaseModel, Field
from typing import Literal


class PromptMessage(BaseModel):
    role: Literal["system", "user","assistant"]
    content: str = Field(min_length=1)


class PromptVersion(BaseModel):
    version: int = Field(ge=1)
    messages: list[PromptMessage] = Field(min_length=1)


class PromptVersionCreate(BaseModel):
    messages: list[PromptMessage] = Field(min_length=1)


class PromptResponse(BaseModel):
    name: str
    version: int
    messages: list[PromptMessage]


class PromptCreate(BaseModel):
    name : str = Field(min_length=1)
    messages : list[PromptMessage]  = Field(min_length=1)


class PromptRenderRequest(BaseModel):
    variables: dict[str,str]


class PromptRenderResponse(BaseModel):
    name: str
    messages : list[PromptMessage]


class PromptExecuteRequest(BaseModel):
    variables: dict[str,str] = Field(default_factory=dict)


class PromptExecuteResponse(BaseModel):
    name: str
    response: str


class PromptStructuredOutput(BaseModel):
    category: str
    reason : str


class PromptTestCase(BaseModel):
    name: str
    variables: dict[str, str]
    expected_messages: list[PromptMessage]


class PromptTestResult(BaseModel):
    name: str
    passed: bool
    actual_messages: list[PromptMessage]
    expected_messages: list[PromptMessage]


class PromptEvaluationResponse(BaseModel):
    prompt_name: str
    version: int
    total_tests: int
    passed_tests: int
    failed_tests: int
    results: list[PromptTestResult]