from findodo.parsers.docling import DoclingParser
from findodo.config import ParserConfig, ChunkerConfig


def test_real_docling_parsing():
    # 1. Setup Configs
    parser_cfg = ParserConfig(name="docling", enable_ocr=True)
    chunker_cfg = ChunkerConfig(chunk_size=500, chunk_overlap=50)

    # 2. Initialize Parser
    print("Initializing Docling (this might take a moment to load models)...")
    parser = DoclingParser(parser_cfg, chunker_cfg)

    # 3. Parse a real PDF
    url = "https://nvidianews.nvidia.com/_gallery/download_pdf/691e34d93d633290a88deeef/"
    
    print(f"Parsing PDF from: {url}")
    chunks = parser.parse(url)

    # 4. Output Results
    print(f"Success! Extracted {len(chunks)} chunks.")
    print("PREVIEW OF CHUNK 1")
    print(chunks[0][:500] + "...")

if __name__ == "__main__":
    test_real_docling_parsing()
