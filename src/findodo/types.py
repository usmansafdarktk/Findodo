from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class FilingItem(str, Enum):
    ITEM_1 = "Item 1"
    ITEM_1A = "Item 1A"
    ITEM_1B = "Item 1B"
    ITEM_2 = "Item 2"
    ITEM_3 = "Item 3"
    ITEM_4 = "Item 4"
    ITEM_5 = "Item 5"
    ITEM_6 = "Item 6"
    ITEM_7 = "Item 7"
    ITEM_7A = "Item 7A"
    ITEM_8 = "Item 8"
    ITEM_9 = "Item 9"
    ITEM_9A = "Item 9A"
    ITEM_9B = "Item 9B"
    ITEM_10 = "Item 10"
    ITEM_11 = "Item 11"
    ITEM_12 = "Item 12"
    ITEM_13 = "Item 13"
    ITEM_14 = "Item 14"
    ITEM_15 = "Item 15"
    ITEM_16 = "Item 16"

class DatasetItem(BaseModel):
    question: str = Field(..., description="The generated question.")
    answer: str = Field(..., description="The answer directly derived from the context.")
    context: str = Field(..., description="The specific text chunk used to generate this QA pair.")

class Dataset(BaseModel):
    items: List[DatasetItem]
