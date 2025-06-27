# backend/types.py
from typing import List, TypedDict

class RecommendedOpening(TypedDict):
    eco: str
    name: str
    style: str
    description: str
    plans: List[str]