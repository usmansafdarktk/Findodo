import re
from typing import List
from edgar import Company, set_identity

from findodo.config import settings
from findodo.types import FilingItem
from findodo.parsers.chunker import Chunker

class SECParser:
    def __init__(self) -> None:
        # Authenticate once upon initialization
        set_identity(settings.sec_identity)
        self.chunker = Chunker()

    def _clean_text(self, text: str) -> str:
        """Standardizes text by removing aggressive whitespace and artifacts."""
        # Remove newline clutter
        text = text.replace("\n", " ").strip()
        # Remove XBRL/table artifacts like "---" or "..."
        text = re.sub(r'-{3,}|\.{3,}', '', text)
        return re.sub(r'\+{2,}', '', text)

    def get_10k_chunks(self, ticker: str, year: int, items: List[FilingItem] | None = None) -> List[str]:
        company = Company(ticker)
        filings = company.get_filings(form="10-K")
        
        #Robust filtering
        filing = next((f for f in filings if f.filing_date.year == year), None)
        if not filing:
             raise ValueError(f"No 10-K found for {ticker} in {year}")

        return self._process_filing(filing.obj(), items)

    def get_10q_chunks(self, ticker: str, year: int, quarter: int, items: List[FilingItem] | None = None) -> List[str]:
        # More robust way to find specific 10-Qs without relying on fragile index files
        company = Company(ticker)
        filings = company.get_filings(form="10-Q")
        
        # Filter by year AND quarter
        filing = next(
            (f for f in filings if f.filing_date.year == year and f.quarter == quarter), 
            None
        )
        if not filing:
             raise ValueError(f"No 10-Q found for {ticker} in {year} Q{quarter}")

        return self._process_filing(filing.obj(), items)

    def _process_filing(self, filing_obj, items_to_filter: List[FilingItem] | None) -> List[str]:
        """Internal helper to extract items, clean them, and chunk them."""
        # If no items specified, grab everything available
        if not items_to_filter:
            selected_items = filing_obj.items
        else:
            # Only keep items that actually exist in this specific filing
            selected_items = [i for i in items_to_filter if i in filing_obj.items]

        raw_texts = [filing_obj[item] for item in selected_items]
        cleaned_text = " ".join([self._clean_text(t) for t in raw_texts])
        
        return self.chunker.split(cleaned_text)
