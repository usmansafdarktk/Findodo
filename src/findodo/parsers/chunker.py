from langchain_text_splitters import TokenTextSplitter


class Chunker:
    """
    Standardized text splitter.
    Refactored to accept configuration arguments instead of using global settings.
    """

    def __init__(self, chunk_size: int, chunk_overlap: int) -> None:
        self._splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def split(self, text: str) -> list[str]:
        return self._splitter.split_text(text)
