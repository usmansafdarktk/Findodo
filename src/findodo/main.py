import hydra
import mlflow
import os
from typing import Dict, Any, cast
from dotenv import load_dotenv
from omegaconf import DictConfig, OmegaConf
from hydra.utils import get_original_cwd

from findodo.config import Config
from findodo.generator import Generator

# Load environment variables immediately
load_dotenv()


# Point Hydra to the 'conf' directory relative to this file
@hydra.main(version_base=None, config_path="../../conf", config_name="config")
def main(cfg: DictConfig) -> None:
    """
    The main application entry point.
    Wraps execution in an MLflow run for scientific tracking.
    """

    # 1. Setup MLflow
    tracking_uri = f"file://{os.path.join(get_original_cwd(), 'mlruns')}"
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("FinDodo_Phase1_Experiments")

    # 2. Start the Run
    with mlflow.start_run() as run:
        print(f"MLflow Run ID: {run.info.run_id}")

        # 3. Log all Hydra parameters
        params = cast(Dict[str, Any], OmegaConf.to_container(cfg, resolve=True))
        mlflow.log_params(params)

        # 4. Validate Config (Pydantic)
        try:
            validated_config = Config(**params)
        except Exception as e:
            print(f"Configuration Error: {e}")
            mlflow.set_tag("status", "failed")
            return

        print("FinDodo initialized successfully!")
        print(f"Output: {validated_config.output_dir}")
        print(f"Parser: {validated_config.parser.name}")
        print(f"Provider: {validated_config.provider.name}")

        # 5. Initialize the Generator
        generator = Generator(validated_config)
        print(f"Instance created: {generator}")

        print("\nSystem is ready. MLflow tracking is active.")


if __name__ == "__main__":
    main()
