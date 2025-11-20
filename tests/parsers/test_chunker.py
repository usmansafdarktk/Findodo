from findodo.parsers.chunker import Chunker


def test_chunker_splits_long_text():
    # Manually inject settings
    chunker = Chunker(chunk_size=10, chunk_overlap=0)
    long_text = "word " * 20
    chunks = chunker.split(long_text)

    assert len(chunks) > 1


def test_chunker_does_not_split_short_text():
    chunker = Chunker(chunk_size=100, chunk_overlap=0)
    short_text = "Short text."
    chunks = chunker.split(short_text)

    assert len(chunks) == 1
