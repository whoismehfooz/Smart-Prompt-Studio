from fastapi import FastAPI, status

from app.exceptions.handlers import register_exception_handler

from app.schemas import (PromptCreate,
                        PromptRenderRequest,
                        PromptRenderResponse,
                        PromptExecuteRequest,
                        PromptExecuteResponse,
                        PromptStructuredOutput,
                        PromptResponse,
                        PromptVersionCreate,
                        PromptTestCase,
                        PromptEvaluationResponse)

from app.services.prompt_service import prompt_service
from app.services.ai_service import ai_service
from app.services.guardrail_service import guardrail_service
from app.middleware.request_logging import request_logging_middleware
from app.logging_config import configure_logging

app = FastAPI(
    title="Smart Prompt Studio",
    description="Backend API for managing and executing reusable AI prompts.",
    version="v1.0.0",
)

app.middleware("http")(request_logging_middleware)
register_exception_handler(app)
configure_logging()


@app.get("/")
async def root():
    return {"message": "Smart Prompt Studio is running"}


@app.get('/health')
async def health_check():
    return {
        "status": "healthy",
        "service": "Smart-Prompt-Studio",
        "version": app.version
    }

@app.post("/prompts", response_model=PromptResponse, status_code=status.HTTP_201_CREATED,
)
async def create_prompt(prompt: PromptCreate):
    return prompt_service.create_prompt(prompt)


@app.post("/prompts/{name}/render", status_code=status.HTTP_200_OK)
async def render_prompt(
    name: str,
    request: PromptRenderRequest):

    return PromptRenderResponse(
        name=name,
        messages=prompt_service.render_prompt(
            name,
            request.variables
        )
    )


@app.post("/prompts/{name}/execute", response_model=PromptExecuteResponse,status_code=status.HTTP_200_OK)
async def execute_prompt(
    name: str,
    request: PromptExecuteRequest,
):
    rendered_messages = prompt_service.render_prompt(
        name,
        request.variables,
    )

    guardrail_service.validate_messages(rendered_messages)

    response = ai_service.execute(rendered_messages)

    return PromptExecuteResponse(
        name=name,
        response=response,
    )


@app.post("/prompts/{name}/execute-structured", response_model=PromptStructuredOutput,status_code=status.HTTP_200_OK)
async def execute_structured_prompt(
    name: str,
    request: PromptExecuteRequest
):
    rendered_messages = prompt_service.render_prompt(
        name,
        request.variables
    )

    response = ai_service.execute_structured(
        rendered_messages
    )

    return response


@app.post("/prompts/{name}/versions", response_model=PromptResponse,status_code=status.HTTP_201_CREATED)
async def create_prompt_version(
    name: str,
    request: PromptVersionCreate
):
    return prompt_service.create_version(
        name,
        request.messages
    )

@app.post("/prompts/{name}/evaluate", response_model=PromptEvaluationResponse, status_code=status.HTTP_200_OK,)
async def evaluate_prompt(
    name: str,
    test_cases: list[PromptTestCase],
    version: int | None = None,
):
    return prompt_service.evaluate_prompt(
        name,
        test_cases,
        version,
    )

@app.get("/prompts/{name}", response_model=PromptResponse, status_code=status.HTTP_200_OK)
async def get_prompt(name: str):
    return prompt_service.get_prompt(name)


@app.get("/prompts/{name}/versions/{version}", response_model=PromptResponse, status_code=status.HTTP_200_OK)
async def get_prompt_version(
    name: str,
    version: int,
):
    return prompt_service.get_prompt_version(name, version)