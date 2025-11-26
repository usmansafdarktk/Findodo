from typing import Any, List
from findodo.core.parsing import BaseParser
from findodo.parsers.chunker import Chunker


class DoclingParser(BaseParser):
    """
    Advanced PDF parser using IBM's Docling for table structure recognition.
    Converts documents to Markdown to preserve table layouts for LLMs.
    """

    def __init__(self, config: Any, chunker_config: Any) -> None:
        super().__init__(config)
        self.chunker = Chunker(chunk_size=chunker_config.chunk_size, chunk_overlap=chunker_config.chunk_overlap)
        self._converter = None

    @property
    def converter(self) -> Any:
        """
        Lazy loader property.
        Only imports and loads the heavy AI models when actually asked for.
        """
        if self._converter is None:
            print("Loading Docling AI models (Lazy Load)...")
            # Import here to prevent top-level crashes
            from docling.document_converter import DocumentConverter

            # Instantiate the DocumentConverter to load the underlying vision models into memory.
            self._converter = DocumentConverter()
        return self._converter

    def parse(self, target: str, **kwargs: Any) -> List[str]:
        """
        Parses a PDF from a local path or URL using Docling.
        target: File path or URL.
        """
        print(f"Docling is analyzing layout for: {target} ...")

        # Docling handles both URLs and local paths automatically
        result = self.converter.convert(target)

        # Export the parsed document structure to Markdown format
        full_text = result.document.export_to_markdown()

        # Split into chunks using our standard chunker
        return self.chunker.split(full_text)
