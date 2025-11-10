from findodo.parsers.chunker import Chunker
from findodo.config import settings


def test_chunker_splits_long_text():
    """Tests that text significantly longer than the chunk size is split."""
    chunker = Chunker()
    # Create a text that is definitely longer than the chunk size
    long_text = "word " * (settings.chunk_size + 100)

    chunks = chunker.split(long_text)

    assert isinstance(chunks, list)
    assert len(chunks) > 1
    assert chunks[0].startswith("word ")


def test_chunker_does_not_split_short_text():
    """Tests that text shorter than the chunk size remains a single chunk."""
    chunker = Chunker()
    short_text = "This is a short text that should not be split."

    chunks = chunker.split(short_text)

    assert isinstance(chunks, list)
    assert len(chunks) == 1
    assert chunks[0] == short_text
