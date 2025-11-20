from io import BytesIO
from typing import Any, List
import requests
from pypdf import PdfReader
from findodo.core.parsing import BaseParser
from findodo.parsers.chunker import Chunker


class PDFParser(BaseParser):
    def __init__(self, config: Any, chunker_config: Any) -> None:
        super().__init__(config)
        # Pass the chunk settings explicitly
        self.chunker = Chunker(chunk_size=chunker_config.chunk_size, chunk_overlap=chunker_config.chunk_overlap)

    def parse(self, target: str, **kwargs: Any) -> List[str]:
        return self.from_url(target)

    def from_url(self, url: str) -> List[str]:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with BytesIO(response.content) as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "

        clean_text = text.replace("\n", " ").strip()
        return self.chunker.split(clean_text)
