from hydra import initialize, compose
from hydra.core.global_hydra import GlobalHydra
from findodo.config import Config


def test_hydra_loads_default_config():
    """
    Tests that Hydra can find the 'conf' directory and load the default 'config.yaml'
    without crashing. This verifies our directory structure is correct.
    """
    # 1. Clear any existing Hydra instance (crucial for testing)
    GlobalHydra.instance().clear()

    # 2. Initialize Hydra pointing to our config directory
    # Relpath is relative to the python script running the test
    with initialize(version_base=None, config_path="../conf"):
        # 3. Compose the configuration (load defaults)
        cfg = compose(config_name="config")

        # 4. Verify it matches our Pydantic schema expectation
        assert cfg.chunker.name == "token"
        assert cfg.parser.name == "sec"
        assert cfg.provider.name == "openai"

        # 5. Verify we can convert it to our strict Pydantic model
        # This ensures the YAML types match the Python types
        validated_config = Config(**cfg)  # type: ignore
        assert validated_config.seed == 42


def test_hydra_overrides():
    """Tests that we can swap components via overrides (just like CLI)."""
    GlobalHydra.instance().clear()

    with initialize(version_base=None, config_path="../conf"):
        # Simulate: python main.py parser=pdf chunker.chunk_size=500
        cfg = compose(config_name="config", overrides=["parser=pdf", "chunker.chunk_size=500"])

        assert cfg.parser.name == "pdf"
        assert cfg.chunker.chunk_size == 500
