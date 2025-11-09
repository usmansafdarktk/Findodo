from abc import ABC, abstractmethod
from typing import List
from findodo.types import DatasetItem

class Provider(ABC):
    @abstractmethod
    def generate_qa(self, text: str, num_questions: int) -> List[DatasetItem]:
        """
        Generates Q&A pairs from a given chunk of text.

        Args:
            text: The financial text chunk to process.
            num_questions: The target number of questions to generate for this chunk.

        Returns:
            A list of validated DatasetItems.
        """
        pass
