import logging
import time

from openai import (
    OpenAI,
    APITimeoutError,
    APIStatusError,
    APIConnectionError,
    RateLimitError,
    AuthenticationError,
)

from app.schemas import (
    PromptMessage,
    PromptStructuredOutput,
)

from app.config import GROQ_API_KEY
from app.exceptions.custom_exceptions import AIProviderError


logger = logging.getLogger(__name__)


class AIService:

    MODEL = "openai/gpt-oss-20b"

    def __init__(self):
        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )

    def execute(self, messages: list[PromptMessage]) -> str:
        try:
            start_time = time.perf_counter()

            logger.info(
                "Starting AI provider execution. model=%s",
                self.MODEL,
            )

            response = self.client.responses.create(
                model=self.MODEL,
                input=[
                    {
                        "role": message.role,
                        "content": message.content,
                    }
                    for message in messages
                ],
            )

            output = response.output_text

            if not output:
                raise AIProviderError(
                    "AI provider returned an empty response.",
                    status_code=502,
                )

            duration = time.perf_counter() - start_time

            logger.info(
                "AI provider execution completed successfully. "
                "model=%s duration=%.3fs",
                self.MODEL,
                duration,
            )

            return output

        except RateLimitError as exc:
            logger.error(
                "AI provider rate limit or quota exceeded: model=%s",
                self.MODEL,
            )
            raise AIProviderError(
                "AI provider rate limit or quota exceeded.",
                status_code=429,
            ) from exc

        except AuthenticationError as exc:
            logger.error(
                "AI provider authentication failed: model=%s",
                self.MODEL,
            )
            raise AIProviderError(
                "AI provider authentication failed.",
                status_code=502,
            ) from exc

        except APITimeoutError as exc:
            logger.error(
                "AI provider request timed out: model=%s",
                self.MODEL,
            )
            raise AIProviderError(
                "AI provider request timed out.",
                status_code=504,
            ) from exc

        except APIConnectionError as exc:
            logger.error(
                "Unable to connect to AI provider: model=%s",
                self.MODEL,
            )
            raise AIProviderError(
                "Unable to connect to AI provider.",
                status_code=503,
            ) from exc

        except APIStatusError as exc:
            logger.error(
                "AI provider returned an error: model=%s",
                self.MODEL,
            )
            raise AIProviderError(
                "AI provider returned an error.",
                status_code=502,
            ) from exc

    def execute_structured(
        self,
        messages: list[PromptMessage],
    ) -> PromptStructuredOutput:

        try:
            start_time = time.perf_counter()

            logger.info(
                "Starting structured AI provider execution. model=%s",
                self.MODEL,
            )

            response = self.client.responses.parse(
                model=self.MODEL,
                input=[
                    {
                        "role": message.role,
                        "content": message.content,
                    }
                    for message in messages
                ],
                text_format=PromptStructuredOutput,
            )

            parsed_output = response.output_parsed

            if parsed_output is None:
                logger.error(
                    "AI provider returned no structured output: model=%s",
                    self.MODEL,
                )
                raise AIProviderError(
                    "AI provider returned no structured output.",
                    status_code=502,
                )

            duration = time.perf_counter() - start_time

            logger.info(
                "Structured AI provider execution completed successfully. "
                "model=%s duration=%.3fs",
                self.MODEL,
                duration,
            )

            return parsed_output

        except RateLimitError as exc:
            logger.error(
                "AI provider rate limit or quota exceeded for structured response: "
                "model=%s",
                self.MODEL,
            )
            raise AIProviderError(
                "AI provider rate limit exceeded.",
                status_code=429,
            ) from exc

        except AuthenticationError as exc:
            logger.error(
                "AI provider authentication failed for structured response: "
                "model=%s",
                self.MODEL,
            )
            raise AIProviderError(
                "AI provider authentication failed.",
                status_code=502,
            ) from exc

        except APITimeoutError as exc:
            logger.error(
                "AI provider structured request timed out: model=%s",
                self.MODEL,
            )
            raise AIProviderError(
                "AI provider request timed out.",
                status_code=504,
            ) from exc

        except APIConnectionError as exc:
            logger.error(
                "Unable to connect to AI provider for structured response: "
                "model=%s",
                self.MODEL,
            )
            raise AIProviderError(
                "Unable to connect to AI provider.",
                status_code=503,
            ) from exc

        except APIStatusError as exc:
            logger.error(
                "AI provider for structured response returned an error: "
                "model=%s",
                self.MODEL,
            )
            raise AIProviderError(
                "AI provider returned an error.",
                status_code=502,
            ) from exc


ai_service = AIService()