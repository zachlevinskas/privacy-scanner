from pydantic import BaseModel
from typing import List

class Quote(BaseModel):
    text: str
    author: str
    tags: List[str]