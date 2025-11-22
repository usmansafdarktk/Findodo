<p align="center">
  <img src="https://github.com/user-attachments/assets/922c6599-15f9-4821-b550-1b4a151c64ad" width="70%" alt="FinDodo Banner">
</p>
FinDodo is an open-source Python library and research framework for generating QA and conversational financial datasets from real-world sources using LLMs. It incorporates systematic experimentation and validation workflows, with the goal of eventually evolving into a unified platform for financial NLP benchmarking.
<br>
It is designed for __Reproducibility__ and **Experimentation**, utilizing **Hydra** for configuration management, **MLflow** for experiment tracking, and **DVC** for data versioning.


## Key Features
* **Plugin Architecture:** Abstract Base Classes allow for the easy integration of new Parsers and Providers without refactoring core logic.
* **Hydra Configuration:** Swap parsers, models, and prompts instantly via the command line, enabling systematic parameter sweeping.
* **Strict Validation:** Pydantic schemas ensure all configurations are type-safe and validated before execution.
* **Experiment Tracking:** Automatic logging of parameters, run metadata, and metrics via MLflow.
* **Prompt Registry:** Manage system prompts as external configuration files to A/B test different generation strategies systematically.


## Installation
This project is managed with **Poetry** for dependencies.

1.  **Clone the repository:**
    ```
    git clone git@github.com:usmansafdarktk/Findodo.git
    cd Findodo
    ```

2.  **Install dependencies:**
    ```
    poetry install
    ```

3.  **Set up environment variables:**
    <br>
    Create a `.env` file in the project root:
    ```
    OPENAI_API_KEY=sk-your-key-here
    ```

## Quick Start
FinDodo is a CLI-first application powered by Hydra. You can run generation tasks directly from the terminal without modifying the source code.

### 1. Basic Run (Default Settings)
Uses the **SEC Parser** (10-K) and **OpenAI Provider** by default.
```
python src/findodo/main.py
```

### 2. Change the Parser
Switch to parsing a PDF instead of an SEC filing.
```
python src/findodo/main.py parser=pdf
```

### 3. Experiment with Parameters
Override specific settings on the fly (e.g., change chunk size or temperature).
```
python src/findodo/main.py chunker.chunk_size=512 provider.temperature=0.7
```

### 4. A/B Test Prompts
Switch between different system prompts defined in the Prompt Registry (``conf/prompt/``).
```
python src/findodo/main.py prompt=creative
```
or

```
python src/findodo/main.py prompt=strict
```

## Running Tests
We maintain a comprehensive test suite including unit tests, integration tests, and configuration verification.
```
# Run all tests
poetry run pytest
```

## 🤝 Contributing
We welcome contributions! The general steps to making a contribution are as follows:
1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
Please see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



