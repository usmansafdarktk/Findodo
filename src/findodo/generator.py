from typing import List, Optional
from tqdm import tqdm

from findodo.config import Config
from findodo.models import Dataset, DatasetItem, FilingItem
from findodo.core.providing import BaseProvider
from findodo.providers.openai import OpenAIProvider
from findodo.parsers.sec import SECParser
from findodo.parsers.pdf import PDFParser


class Generator:
    """
    The main entry point.
    Now fully configurable via Hydra+Pydantic.
    """

    def __init__(self, config: Config, provider: Optional[BaseProvider] = None):
        # 1. Store the config
        self.config = config
        
        # 2. Initialize Provider (Inject config)
        self.provider = provider or OpenAIProvider(config.provider)
        
        # 3. Initialize Parsers (Inject specific parser config AND chunker config)
        self.sec_parser = SECParser(config.parser, config.chunker)
        self.pdf_parser = PDFParser(config.parser, config.chunker)

    def generate_from_texts(self, texts: List[str], total_questions: int = 10) -> Dataset:
        results: List[DatasetItem] = []
        num_chunks = len(texts)
        if num_chunks == 0:
            return Dataset(items=[])

        base_questions = total_questions // num_chunks
        extra_questions = total_questions % num_chunks

        with tqdm(total=total_questions, desc="Generating Q&A pairs", colour="green") as pbar:
            for i, text in enumerate(texts):
                questions_for_chunk = base_questions + (1 if i < extra_questions else 0)

                if questions_for_chunk > 0:
                    new_items = self.provider.generate_qa(text, questions_for_chunk)
                    results.extend(new_items)
                    pbar.update(len(new_items))

        return Dataset(items=results[:total_questions])

    def generate_from_sec(
        self,
        ticker: str,
        year: int,
        quarter: int | None = None,
        items: List[FilingItem] | None = None,
        total_questions: int = 10,
    ) -> Dataset:
        if quarter:
            print(f"Fetching 10-Q for {ticker} Q{quarter} {year}...")
            chunks = self.sec_parser.parse(ticker, year=year, quarter=quarter, items=items)
        else:
            print(f"Fetching 10-K for {ticker} {year}...")
            chunks = self.sec_parser.parse(ticker, year=year, items=items)

        print(f"Processing {len(chunks)} text chunks...")
        return self.generate_from_texts(chunks, total_questions)

    def generate_from_pdf(self, url: str, total_questions: int = 10) -> Dataset:
        print(f"Downloading and parsing PDF from {url}...")
        chunks = self.pdf_parser.parse(url)
        print(f"Processing {len(chunks)} text chunks...")
        return self.generate_from_texts(chunks, total_questions)
