import json
from typing import List, Any
from openai import OpenAI, OpenAIError
from openai.types.chat import ChatCompletionToolParam
from pydantic import ValidationError
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type

from findodo.models import DatasetItem
from findodo.core.providing import BaseProvider
from findodo.prompts import DEFAULT_SYSTEM_PROMPT

class OpenAIProvider(BaseProvider):
    def __init__(self, config: Any):
        super().__init__(config)
        # Logic: Use API key from config if present, otherwise rely on env var (handled by OpenAI client)
        api_key = config.api_key.get_secret_value() if config.api_key else None
        
        self.client = OpenAI(api_key=api_key)
        self.model = config.model
        self.temperature = config.temperature

    @property
    def _tool_schema(self) -> List[ChatCompletionToolParam]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "generate_dataset",
                    "description": "Generates a list of financial QA pairs.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "question": {"type": "string"},
                                        "answer": {"type": "string"},
                                        "context": {"type": "string"},
                                    },
                                    "required": ["question", "answer", "context"],
                                },
                            }
                        },
                        "required": ["items"],
                    },
                },
            }
        ]

    @retry(
        wait=wait_random_exponential(multiplier=1, max=60),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(OpenAIError),
    )
    def generate_qa(self, text: str, num_questions: int) -> List[DatasetItem]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Generate {num_questions} questions for this text: {text}"},
                ],
                tools=self._tool_schema,
                tool_choice={"type": "function", "function": {"name": "generate_dataset"}},
                temperature=self.temperature,
            )

            message = response.choices[0].message

            if not message.tool_calls:
                print("Warning: Model did not call the generation tool.")
                return []

            tool_call = message.tool_calls[0]
            # MyPy Guard: Ensure it's a function tool
            if tool_call.type != "function":
                return []
            arguments = json.loads(tool_call.function.arguments)

            valid_items = []
            for item in arguments.get("items", []):
                try:
                    valid_items.append(DatasetItem(**item))
                except ValidationError:
                    print("Warning: Dropped one malformed QA pair (missing fields).")
                    continue

            return valid_items

        except Exception as e:
            print(f"Error parsing OpenAI response: {e}")
            return []
