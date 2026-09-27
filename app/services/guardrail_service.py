import logging

from app.schemas import PromptMessage
from app.exceptions.custom_exceptions import PromptGuardrailError


logger = logging.getLogger(__name__)


class GuardrailService:

    MAX_MESSAGE_LENGTH = 10_000
    MAX_TOTAL_PROMPT_LENGTH = 30_000

    def validate_messages(
        self,
        messages: list[PromptMessage],
    ) -> None:

        logger.info("Guardrail validation started.")

        if not messages:

            logger.warning("Guardrail rejected prompt: no messages provided.")

            raise PromptGuardrailError("Prompt must contain at least one message.")

        total_length = 0

        for message in messages:

            if not message.content.strip():

                logger.warning("Guardrail rejected prompt: empty message content.")

                raise PromptGuardrailError(
                    "Prompt message content cannot be empty."
                )

            if len(message.content) > self.MAX_MESSAGE_LENGTH:
                raise PromptGuardrailError(
                    "Prompt message exceeds the maximum allowed length."
                )

            total_length += len(message.content)

        if total_length > self.MAX_TOTAL_PROMPT_LENGTH:
            raise PromptGuardrailError(
                "Total prompt length exceeds the maximum allowed length."
            )

        logger.info("Guardrail validation passed.")


guardrail_service = GuardrailService()