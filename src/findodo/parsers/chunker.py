from langchain_text_splitters import TokenTextSplitter
from findodo.config import settings


class Chunker:
    """
    Standardized text splitter to ensure all documents fit into LLM context windows.
    Uses settings from config.py for uniformity across the entire library.
    """

    def __init__(self) -> None:
        self._splitter = TokenTextSplitter(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)

    def split(self, text: str) -> list[str]:
        return self._splitter.split_text(text)
