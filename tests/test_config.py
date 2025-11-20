from findodo.config import Config, ChunkerConfig, ParserConfig, ProviderConfig

def test_config_structure():
    """Tests that we can manually instantiate the config."""
    # Simulate data from Hydra
    cfg = Config(
        chunker=ChunkerConfig(chunk_size=512),
        parser=ParserConfig(name="sec"),
        provider=ProviderConfig(name="openai", model="gpt-3.5"),
        seed=123
    )
    assert cfg.chunker.chunk_size == 512
    assert cfg.seed == 123
