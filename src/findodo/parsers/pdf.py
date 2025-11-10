from io import BytesIO
import requests
from pypdf import PdfReader
from findodo.parsers.chunker import Chunker


class PDFParser:
    def __init__(self) -> None:
        self.chunker = Chunker()

    def from_url(self, url: str) -> list[str]:
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
