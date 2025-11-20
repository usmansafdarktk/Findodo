from typing import Optional
from pydantic import BaseModel, Field, SecretStr


#  Sub-Configurations 
class ChunkerConfig(BaseModel):
    name: str = "token"
    chunk_size: int = Field(1024, gt=0, description="Tokens per chunk")
    chunk_overlap: int = Field(100, ge=0, description="Overlap between chunks")

class ParserConfig(BaseModel):
    name: str
    include_tables: bool = Field(False, description="Whether to parse tables separately")
    # We allow extra fields because different parsers (SEC vs PDF) have different settings
    model_config = {"extra": "allow"}

class ProviderConfig(BaseModel):
    name: str
    model: str
    api_key: Optional[SecretStr] = Field(None, description="API Key (loaded from env if None)")
    temperature: float = Field(0.0, ge=0.0, le=1.0)
    # Allow extra fields for different providers (OpenAI vs Azure)
    model_config = {"extra": "allow"}


#  Master Configuration 
class Config(BaseModel):
    """
    The Master Configuration Object.
    Hydra will populate this from YAMLs, and Pydantic will validate strict types.
    """
    # Sub-configs
    chunker: ChunkerConfig
    parser: ParserConfig
    provider: ProviderConfig

    # Global settings
    seed: int = 42
    output_dir: str = "data/processed"
    
    # Allow Hydra's internal keys (like hydra.run.dir) to exist without crashing Pydantic
    model_config = {"extra": "ignore"}
