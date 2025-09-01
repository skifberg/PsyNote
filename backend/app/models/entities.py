from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    item_id: str
    text: str
    domain: str
    facet: str
    keyed_direction: str

class UserResponse(BaseModel):
    user_id: int
    item_id: str
    score: int
    response_time: Optional[int] = None

class TestResult(BaseModel):
    user_id: int
    test_type: str = "big5"
    extraversion: Optional[float] = None
    agreeableness: Optional[float] = None
    conscientiousness: Optional[float] = None
    neuroticism: Optional[float] = None
    openness: Optional[float] = None
    