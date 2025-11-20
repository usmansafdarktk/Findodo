import re
from typing import List, Any
from edgar import Company, set_identity

from findodo.models import FilingItem
from findodo.core.parsing import BaseParser
from findodo.parsers.chunker import Chunker


class SECParser(BaseParser):
    def __init__(self, config: Any, chunker_config: Any) -> None:
        super().__init__(config)
        # Initialize Chunker by passing values from the config
        self.chunker = Chunker(chunk_size=chunker_config.chunk_size, chunk_overlap=chunker_config.chunk_overlap)

        # For Phase 1, we set a default identity or assume EDGAR_IDENTITY env var is set.
        # In Phase 2, we will move this explicitly into the ParserConfig.
        try:
            set_identity("FinDodo Research findodo@example.com")
        except Exception:
            pass

    def _clean_text(self, text: str) -> str:
        text = text.replace("\n", " ").strip()
        text = re.sub(r"-{3,}|\.{3,}", "", text)
        return re.sub(r"\+{2,}", "", text)

    def parse(self, target: str, **kwargs: Any) -> List[str]:
        # Logic to route between 10-K and 10-Q based on kwargs
        year = kwargs.get("year")
        if not year:
            raise ValueError("Year is required for SEC parsing")

        items = kwargs.get("items")
        quarter = kwargs.get("quarter")

        if quarter:
            return self.get_10q_chunks(target, year, quarter, items)
        else:
            return self.get_10k_chunks(target, year, items)

    def get_10k_chunks(self, ticker: str, year: int, items: List[FilingItem] | None = None) -> List[str]:
        company = Company(ticker)
        filings = company.get_filings(form="10-K")
        filing = next((f for f in filings if f.filing_date.year == year), None)
        if not filing:
            raise ValueError(f"No 10-K found for {ticker} in {year}")
        return self._process_filing(filing.obj(), items)

    def get_10q_chunks(self, ticker: str, year: int, quarter: int, items: List[FilingItem] | None = None) -> List[str]:
        company = Company(ticker)
        filings = company.get_filings(form="10-Q")
        filing = next((f for f in filings if f.filing_date.year == year and f.quarter == quarter), None)
        if not filing:
            raise ValueError(f"No 10-Q found for {ticker} in {year} Q{quarter}")
        return self._process_filing(filing.obj(), items)

    def _process_filing(self, filing_obj: Any, items_to_filter: List[FilingItem] | None) -> List[str]:
        if not items_to_filter:
            selected_items = filing_obj.items
        else:
            selected_items = [i for i in items_to_filter if i in filing_obj.items]

        raw_texts = [filing_obj[item] for item in selected_items]
        cleaned_text = " ".join([self._clean_text(t) for t in raw_texts])

        return self.chunker.split(cleaned_text)
