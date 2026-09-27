from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    PromptAlreadyExistsError,
    PromptNotFoundError,
    PromptVariableError,
    AIProviderError,
    PromptVersionNotFoundError,
    PromptGuardrailError
)


def register_exception_handler(app:FastAPI):
    @app.exception_handler(PromptAlreadyExistsError)
    async def prompt_already_exists_handler(
        request: Request,
        exc: PromptAlreadyExistsError,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PromptNotFoundError)
    async def prompt_not_found_handler(
        request: Request,
        exc: PromptNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PromptVariableError)
    async def prompt_variable_error_handler(
            request: Request,
            exc: PromptVariableError
    ):
        return JSONResponse(
            status_code=422,
            content={"detail": str(exc)}
        )

    @app.exception_handler(AIProviderError)
    async def ai_provider_error_handler(
        request: Request,
        exc: AIProviderError
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": str(exc)}
        )

    @app.exception_handler(PromptVersionNotFoundError)
    async def prompt_version_not_found_handler(
        request: Request,
        exc: PromptVersionNotFoundError
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )

    @app.exception_handler(PromptGuardrailError)
    async def guardrail_error_handler(
        request: Request,
        exc: PromptGuardrailError
    ):
        return JSONResponse(
            status_code=400,
            content={"detail":str(exc)}
        )