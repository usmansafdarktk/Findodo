from abc import ABC, abstractmethod
from typing import List, Any


class BaseParser(ABC):
    """
    The contract that all Parsers (SEC, PDF, Docling) must follow.
    """

    def __init__(self, config: Any):
        """
        All parsers are initialized with their specific sub-config.
        """
        self.config = config

    @abstractmethod
    def parse(self, target: str, **kwargs: Any) -> List[str]:
        """
        Parses a target (URL, Ticker, or File Path) into text chunks.

        Args:
            target: The ticker (e.g., "AAPL") or file path.
            kwargs: Extra arguments (like 'year', 'quarter' for SEC).

        Returns:
            A list of text chunks ready for the LLM.
        """
        pass
