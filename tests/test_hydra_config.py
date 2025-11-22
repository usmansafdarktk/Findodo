from hydra import initialize, compose
from hydra.core.global_hydra import GlobalHydra
from findodo.config import Config


def test_hydra_loads_default_config():
    """
    Tests that Hydra can find the 'conf' directory and load the default 'config.yaml'.
    Now also verifies the PROMPT REGISTRY.
    """
    GlobalHydra.instance().clear()

    with initialize(version_base=None, config_path="../conf"):
        cfg = compose(config_name="config")

        # 1. Check standard components
        assert cfg.chunker.name == "token"
        assert cfg.parser.name == "sec"
        assert cfg.provider.name == "openai"

        # 2. Check Prompt Registry
        assert cfg.prompt.name == "default"
        assert "You are an expert" in cfg.prompt.system_prompt

        # 3. Verify Pydantic Validation
        validated_config = Config(**cfg)
        assert validated_config.seed == 42


def test_hydra_overrides():
    """Tests that we can swap components via overrides."""
    GlobalHydra.instance().clear()

    with initialize(version_base=None, config_path="../conf"):
        # Simulate: python main.py parser=pdf chunker.chunk_size=500
        cfg = compose(config_name="config", overrides=["prompt.name=custom", "chunker.chunk_size=500"])

        assert cfg.prompt.name == "custom"
        assert cfg.chunker.chunk_size == 500
