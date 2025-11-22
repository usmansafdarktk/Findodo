from findodo.generator import Generator
from findodo.config import Config, ChunkerConfig, ParserConfig, ProviderConfig


def test_generator_initialization():
    """
    Tests that the Generator correctly initializes all sub-components
    when provided with a valid Config object.
    """
    # 1. Create a full valid configuration
    full_config = Config(
        chunker=ChunkerConfig(chunk_size=100, chunk_overlap=10),
        parser=ParserConfig(name="sec", include_tables=False),
        provider=ProviderConfig(name="openai", model="gpt-test"),
        seed=999,
        output_dir="data/test",
    )

    # 2. Initialize Generator
    gen = Generator(full_config)

    # 3. Assertions: Check if children were created with correct settings

    # Check SEC Parser
    assert gen.sec_parser.config.include_tables is False
    # Check if chunker config flowed down to SEC Parser's chunker
    # Note: This assumes SECParser stores its chunker as self.chunker
    # We can check the internal splitter attributes if exposed, or just existence
    assert gen.sec_parser.chunker is not None

    # Check PDF Parser
    assert gen.pdf_parser.config.name == "sec"  # It uses the passed parser config
    assert gen.pdf_parser.chunker is not None

    # Check Provider
    assert gen.provider.model == "gpt-test"
