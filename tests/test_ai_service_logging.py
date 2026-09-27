from unittest.mock import Mock

from app.schemas import PromptMessage
from app.services.ai_service import AIService


def test_ai_service_logs_success(caplog):
    service = AIService()

    mock_response = Mock()
    mock_response.output_text = "Category: account"

    service.client.responses.create = Mock(
        return_value=mock_response
    )

    messages = [
        PromptMessage(
            role="user",
            content="I cannot reset my password."
        )
    ]

    with caplog.at_level("INFO"):
        result = service.execute(messages)

    assert result == "Category: account"

    assert "Starting AI provider execution. model=openai/gpt-oss-20b" in caplog.text
    assert "AI provider execution completed successfully. model=openai/gpt-oss-20b" in caplog.text