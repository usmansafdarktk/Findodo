import os
from findodo.config import settings

def test_settings_load_from_env():
    """Tests that the config loader finds the .env file and loads the key."""
    assert settings.openai_api_key.get_secret_value() == os.environ.get("OPENAI_API_KEY")
    assert settings.default_model is not None
    assert settings.sec_identity is not None
