from abc import ABC, abstractmethod
from typing import List, Any
from findodo.models import DatasetItem


class BaseProvider(ABC):
    """
    The contract that all LLM Providers (OpenAI, Azure, Local) must follow.
    """

    def __init__(self, config: Any, prompt_config: Any):
        """
        All providers are initialized with their specific sub-config.
        """
        self.config = config
        self.prompt_config = prompt_config

    @abstractmethod
    def generate_qa(self, text: str, num_questions: int) -> List[DatasetItem]:
        """
        Generates Q&A pairs from a single chunk of text.

        Args:
            text: The text chunk context.
            num_questions: How many pairs to generate.

        Returns:
            A list of validated DatasetItems.
        """
        pass
