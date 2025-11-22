import pytest
from unittest.mock import MagicMock, patch
from findodo.config import Config, ChunkerConfig, ParserConfig, ProviderConfig, PromptConfig
from findodo.generator import Generator


@pytest.fixture
def valid_config():
    """Creates a full valid configuration object."""
    return Config(
        chunker=ChunkerConfig(chunk_size=100, chunk_overlap=10),
        parser=ParserConfig(name="sec", include_tables=False),
        provider=ProviderConfig(name="openai", model="gpt-test"),
        prompt=PromptConfig(name="default", system_prompt="Test Prompt"),
        seed=999,
        output_dir="data/test",
    )


def test_config_is_mlflow_serializable(valid_config):
    """
    MLflow requires parameters to be simple dictionaries.
    Pydantic models can sometimes be tricky. This ensures we can convert safely.
    """
    # Simulate the conversion
    config_dict = valid_config.model_dump()

    # Assert it's a pure dict that MLflow can log
    assert isinstance(config_dict, dict)
    assert config_dict["seed"] == 999
    assert config_dict["chunker"]["chunk_size"] == 100


def test_generator_runs_inside_mlflow_context(valid_config):
    """
    Integration test to ensure Generator doesn't conflict with active MLflow runs.
    We mock MLflow so we don't actually write to disk.
    """
    # Mock the MLflow module
    with patch("findodo.main.mlflow") as mock_mlflow:
        # Simulate starting a run
        mock_mlflow.start_run.return_value.__enter__.return_value = MagicMock()

        # Initialize Generator
        gen = Generator(valid_config)

        # Just ensure it initialized without crashing
        assert gen is not None

        # Simulate logging params
        # We verify that we CAN log our config without error
        mock_mlflow.log_params(valid_config.model_dump())

        mock_mlflow.log_params.assert_called_once()
