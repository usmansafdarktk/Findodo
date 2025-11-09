import json
from typing import List, Any, Dict
from openai import OpenAI, OpenAIError
from pydantic import ValidationError
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type

from findodo.config import settings
from findodo.types import DatasetItem
from findodo.providers.base import Provider
from findodo.prompts import DEFAULT_SYSTEM_PROMPT

class OpenAIProvider(Provider):
    def __init__(self, model: str | None = None):
        self.client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
        self.model = model or settings.default_model

    @property
    def _tool_schema(self) -> List[Dict[str, Any]]:
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
        retry=retry_if_exception_type(OpenAIError)
    )
    def generate_qa(self, text: str, num_questions: int) -> List[DatasetItem]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Generate {num_questions} questions for this text: {text}"}
                ],
                tools=self._tool_schema,
                tool_choice={"type": "function", "function": {"name": "generate_dataset"}},
                temperature=0.0,
            )

            tool_call = response.choices[0].message.tool_calls[0]
            arguments = json.loads(tool_call.function.arguments)
            
            # Validate with Pydantic immediately
            valid_items = []
            for item in arguments.get("items", []):
                try:
                    # Try to validate this specific item
                    valid_items.append(DatasetItem(**item))
                except ValidationError:
                    # If it fails, just log a warning and KEEP GOING.
                    # Don't crash the whole process for one bad LLM output.
                    print(f"Warning: Dropped one malformed QA pair (missing fields).")
                    continue
            
            return valid_items

        except (IndexError, json.JSONDecodeError, AttributeError) as e:
            print(f"Error parsing OpenAI response: {e}")
            return []
