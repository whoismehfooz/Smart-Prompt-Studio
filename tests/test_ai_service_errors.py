import pytest
import httpx2
from openai import (RateLimitError,
                    AuthenticationError,
                    APITimeoutError,
                    APIConnectionError,
                    APIStatusError)

from app.exceptions.custom_exceptions import AIProviderError
from app.services.ai_service import AIService



def test_rate_limit_error():

    service = AIService()

    http_request = httpx2.Request(
        "POST",
        "https://api.groq.com/openai/v1/responses"
    )

    http_response = httpx2.Response(
        429,
        request=http_request
    )

    def raise_rate_limit(*args,**kwargs):
        raise RateLimitError(
            "rate limited",
            response=http_response,
            body=None
        )

    service.client.responses.create = raise_rate_limit

    with pytest.raises(AIProviderError) as exc_info:
        service.execute([])

    assert exc_info.value.status_code == 429
    assert str(exc_info.value) == (
        "AI provider rate limit or quota exceeded."
    )



def test_authentication_error():

    service = AIService()

    http_request = httpx2.Request(
        "POST",
        "https://api.groq.com/openai/v1/responses"
    )

    http_response = httpx2.Response(
        401,
        request=http_request
    )

    def raise_authentication_error(*args,**kwargs):
        raise AuthenticationError(
            "invalid api key",
            response=http_response,
            body=None
        )

    service.client.responses.create = raise_authentication_error

    with pytest.raises(AIProviderError) as exc_info:
        service.execute([])

    assert exc_info.value.status_code == 502
    assert str(exc_info.value) == (
        "AI provider authentication failed."
    )


def test_api_timeout_error():

    service = AIService()

    http_request = httpx2.Request(
        "POST",
        "https://api.groq.com/openai/v1/responses"
    )
    def raise_time_out_error(*args,**kwargs):
        raise APITimeoutError(
            request=http_request
        )

    service.client.responses.create = raise_time_out_error

    with pytest.raises(AIProviderError) as exc_info:
        service.execute([])

    assert exc_info.value.status_code == 504
    assert str(exc_info.value) == (
        "AI provider request timed out."
    )


def test_api_connection_error():

    service = AIService()

    http_request = httpx2.Request(
        "POST",
        "https://api.groq.com/openai/v1/responses"
    )

    def raise_connection_error(*args,**kwargs):
        raise APIConnectionError(
            request=http_request,
        )

    service.client.responses.create = raise_connection_error

    with pytest.raises(AIProviderError) as exc_info:
        service.execute([])

    assert exc_info.value.status_code == 503
    assert str(exc_info.value) == (
        "Unable to connect to AI provider."
    )


def test_api_status_error():

    service = AIService()

    http_reqest = httpx2.Request(
        "POST",
        "https://api.groq.com/openai/v1/responses"
    )

    http_response = httpx2.Response(
        500,
        request=http_reqest
    )

    def raise_connection_error(*args,**kwargs):
        raise APIStatusError(
            "provider server error",
            response=http_response,
            body=None
        )

    service.client.responses.create = raise_connection_error

    with pytest.raises(AIProviderError) as exc_info:
        service.execute([])

    assert exc_info.value.status_code == 502
    assert str(exc_info.value) == (
        "AI provider returned an error."
    )


def test_empty_provider_response():

    service = AIService()

    class FakeResponse:
        output_text = ""

    def return_empty_response(*args,**kwargs):
        return FakeResponse()

    service.client.responses.create = return_empty_response

    with pytest.raises(AIProviderError) as exc_info:
        service.execute([])

    assert exc_info.value.status_code == 502
    assert str(exc_info.value) == (
        "AI provider returned an empty response."
    )