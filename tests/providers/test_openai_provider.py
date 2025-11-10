import json
import pytest
from unittest.mock import MagicMock
from findodo.providers.openai import OpenAIProvider

# 1. Define mock payloads from the OpenAI API

# This is what a "good" response looks like
GOOD_PAYLOAD = {
    "items": [{"question": "q1", "answer": "a1", "context": "c1"}, {"question": "q2", "answer": "a2", "context": "c2"}]
}

# This is the "bad" response (The second item is missing the 'context' field)
# that crashed the old library
BAD_PAYLOAD_MISSING_FIELD = {
    "items": [{"question": "q1", "answer": "a1", "context": "c1"}, {"question": "q_bad", "answer": "a_bad"}]
}


# Helper function to create the complex, nested mock object
def create_mock_api_response(payload):
    mock_response = MagicMock()
    mock_tool_call = MagicMock()
    # The API returns the payload as a JSON *string* in `arguments`
    mock_tool_call.function.arguments = json.dumps(payload)

    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.tool_calls = [mock_tool_call]
    return mock_response


@pytest.fixture
def provider():
    """Creates a fresh provider instance for each test."""
    return OpenAIProvider()


def test_generate_qa_success(provider, monkeypatch):
    """Tests the happy path: a good API response is parsed correctly."""
    # 1. Create a mock for the client's `create` method
    mock_create = MagicMock(return_value=create_mock_api_response(GOOD_PAYLOAD))

    # 2. "monkeypatch" the real client, replacing its `create` method with our mock
    monkeypatch.setattr(provider.client.chat.completions, "create", mock_create)

    # 3. Run the function
    result = provider.generate_qa("some text", 2)

    # 4. Assert
    assert len(result) == 2
    assert result[0].question == "q1"
    assert result[1].answer == "a2"
    mock_create.assert_called_once()  # Ensure the mock was actually called


def test_generate_qa_robustness_skips_bad_item(provider, monkeypatch, capsys):
    """
    Tests our bug fix!
    Ensures that when the API returns a malformed item,
    we log a warning and return *only* the valid items, NOT crash.
    """
    # 1. Mock the `create` method to return the BAD payload
    mock_create = MagicMock(return_value=create_mock_api_response(BAD_PAYLOAD_MISSING_FIELD))
    monkeypatch.setattr(provider.client.chat.completions, "create", mock_create)

    # 2. Run the function
    result = provider.generate_qa("some text", 2)

    # 3. Assert: The key test! We should get 1 valid item back, not 0 and not a crash
    assert len(result) == 1
    assert result[0].question == "q1"

    # 4. Assert that we printed the warning
    captured = capsys.readouterr()  # capsys is a pytest fixture to capture print()
    assert "Warning: Dropped one malformed QA pair" in captured.out
