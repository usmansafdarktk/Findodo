import json
import pytest
from unittest.mock import MagicMock
from findodo.providers.openai import OpenAIProvider
from findodo.config import ProviderConfig, PromptConfig

# 1. Define mock payloads from the OpenAI API

# This is what a "good" response looks like
GOOD_PAYLOAD = {
    "items": [{"question": "q1", "answer": "a1", "context": "c1"}, {"question": "q2", "answer": "a2", "context": "c2"}]
}

# This is the "bad" response (The second item is missing the 'context' field)
BAD_PAYLOAD_MISSING_FIELD = {
    "items": [{"question": "q1", "answer": "a1", "context": "c1"}, {"question": "q_bad", "answer": "a_bad"}]
}


# Helper function to create the complex, nested mock object
def create_mock_api_response(payload):
    mock_response = MagicMock()
    mock_tool_call = MagicMock()

    # The API returns the payload as a JSON *string* in `arguments`
    mock_tool_call.type = "function"
    mock_tool_call.function.arguments = json.dumps(payload)

    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.tool_calls = [mock_tool_call]
    return mock_response


@pytest.fixture
def provider():
    """Creates a fresh provider instance for each test with mock configs."""
    # 1. Create dummy Provider Config
    config = ProviderConfig(name="openai", model="gpt-4-test", temperature=0.0, api_key="sk-fake-key-for-testing")

    # 2. Create dummy Prompt Config
    prompt_config = PromptConfig(name="default", system_prompt="You are a helpful assistant.")

    # 3. Inject both into the Provider
    return OpenAIProvider(config, prompt_config)


def test_generate_qa_success(provider, monkeypatch):
    """Tests the happy path: a good API response is parsed correctly."""
    mock_create = MagicMock(return_value=create_mock_api_response(GOOD_PAYLOAD))
    monkeypatch.setattr(provider.client.chat.completions, "create", mock_create)

    result = provider.generate_qa("some text", 2)

    assert len(result) == 2
    assert result[0].question == "q1"
    assert result[1].answer == "a2"

    # Verify that the system prompt was actually passed to the API
    call_args = mock_create.call_args
    # The 'messages' list is the 2nd argument in the call kwargs
    messages = call_args.kwargs["messages"]
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "You are a helpful assistant."


def test_generate_qa_robustness_skips_bad_item(provider, monkeypatch, capsys):
    """
    Tests our bug fix!
    Ensures that when the API returns a malformed item,
    we log a warning and return *only* the valid items, NOT crash.
    """
    mock_create = MagicMock(return_value=create_mock_api_response(BAD_PAYLOAD_MISSING_FIELD))
    monkeypatch.setattr(provider.client.chat.completions, "create", mock_create)

    result = provider.generate_qa("some text", 2)

    assert len(result) == 1
    assert result[0].question == "q1"

    captured = capsys.readouterr()
    assert "Warning: Dropped one malformed QA pair" in captured.out
