# FinDodo

A Python library for generating question-answer datasets from financial documents using LLMs.

## Installation

This project is managed with Poetry.

1.  Clone the repository:
    ```
    git clone [https://github.com/your-username/findodo.git](https://github.com/your-username/findodo.git)
    cd findodo
    ```

2.  Install dependencies:
    ```
    poetry install
    ```

3.  Set up environment variables by creating a `.env` file in the project root:
    ```
    OPENAI_API_KEY=sk-your-key-here
    ```

## Basic Usage

The `Generator` class is the main entry point for all operations. It automatically handles data parsing, chunking, and LLM orchestration.

```
from findodo import Generator, FilingItem

# Initialize the generator
generator = Generator()

# Example 1: Generate from an SEC 10-K
dataset_10k = generator.generate_from_sec(
    ticker="AAPL",
    year=2023,
    items=[FilingItem.ITEM_1A], # Specify sections, e.g., Risk Factors
    total_questions=5
)
print(dataset_10k.items)

# Example 2: Generate from a PDF URL
dataset_pdf = generator.generate_from_pdf(
    url="[https://www.berkshirehathaway.com/letters/2023ltr.pdf](https://www.berkshirehathaway.com/letters/2023ltr.pdf)",
    total_questions=3
)
print(dataset_pdf.items)

#  Example 3: Generate from raw text 
my_texts = [
    "In 2023, revenue was $10 billion.",
    "In 2022, revenue was $8 billion."
]
dataset_text = generator.generate_from_texts(
    texts=my_texts,
    total_questions=2
)
print(dataset_text.items)
```
