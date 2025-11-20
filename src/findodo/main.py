import hydra
from dotenv import load_dotenv
from omegaconf import DictConfig, OmegaConf
from findodo.config import Config
from findodo.generator import Generator

# Load environment variables from .env file immediately
load_dotenv()


# Point Hydra to the 'conf' directory relative to this file
@hydra.main(version_base=None, config_path="../../conf", config_name="config")
def main(cfg: DictConfig) -> None:
    """
    The main application entry point.
    1. Loads YAML config via Hydra.
    2. Validates it via Pydantic.
    3. Initializes the Generator.
    """

    # 1. Validate Config
    # Convert Hydra's internal format to a standard Python dictionary
    raw_config = OmegaConf.to_container(cfg, resolve=True)

    try:
        # Pass it through our strict Pydantic model
        # If kwargs like 'ticker' are passed, they are ignored by Pydantic
        # (due to extra="ignore") but remain in 'cfg' for us to use later.
        validated_config = Config(**raw_config)  # type: ignore
    except Exception as e:
        print(f"Configuration Error: {e}")
        return

    print("FinDodo initialized successfully!")
    print(f" Output: {validated_config.output_dir}")
    print(f" Parser: {validated_config.parser.name}")
    print(f" Provider: {validated_config.provider.name}")

    # 2. Initialize the Generator
    # This proves that our Dependency Injection works
    generator = Generator(validated_config)

    print(f"Instance created: {generator}")

    print("\nSystem is ready. Use command line arguments to run specific tasks.")
    print("   Example: python src/findodo/main.py parser=pdf")


if __name__ == "__main__":
    main()
