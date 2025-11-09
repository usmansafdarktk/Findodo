from typing import List, Type
from tqdm import tqdm

from findodo.types import Dataset, DatasetItem, FilingItem
from findodo.providers.base import Provider
from findodo.providers.openai import OpenAIProvider
from findodo.parsers.sec import SECParser
from findodo.parsers.pdf import PDFParser

class Generator:
    """
    The main entry point for FinDodo.
    Orchestrates the flow between Data Parsers and LLM Providers.
    """
    def __init__(self, provider: Provider | None = None):
        # Dependency Injection: Use the provided LLM, or default to OpenAI
        self.provider = provider or OpenAIProvider()
        self.sec_parser = SECParser()
        self.pdf_parser = PDFParser()

    def generate_from_texts(self, texts: List[str], total_questions: int = 10) -> Dataset:
        """
        Generates a dataset from a raw list of text chunks.
        Distributes the question budget across the chunks.
        """
        results: List[DatasetItem] = []
        num_chunks = len(texts)
        if num_chunks == 0:
            return Dataset(items=[])

        # Simple distribution of questions per chunk
        base_questions = total_questions // num_chunks
        extra_questions = total_questions % num_chunks

        with tqdm(total=total_questions, desc="Generating Q&A pairs", colour="green") as pbar:
            for i, text in enumerate(texts):
                # Calculate how many questions this specific chunk needs
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
        total_questions: int = 10
    ) -> Dataset:
        """Generates a dataset from an SEC filing (10-K or 10-Q)."""
        if quarter:
            print(f"Fetching 10-Q for {ticker} Q{quarter} {year}...")
            chunks = self.sec_parser.get_10q_chunks(ticker, year, quarter, items)
        else:
            print(f"Fetching 10-K for {ticker} {year}...")
            chunks = self.sec_parser.get_10k_chunks(ticker, year, items)

        print(f"Processing {len(chunks)} text chunks...")
        return self.generate_from_texts(chunks, total_questions)

    def generate_from_pdf(self, url: str, total_questions: int = 10) -> Dataset:
        """Generates a dataset from a PDF URL."""
        print(f"Downloading and parsing PDF from {url}...")
        chunks = self.pdf_parser.from_url(url)
        print(f"Processing {len(chunks)} text chunks...")
        return self.generate_from_texts(chunks, total_questions)
