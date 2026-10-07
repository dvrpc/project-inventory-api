from pydantic import BaseModel
from typing import Optional


class TopicResponse(BaseModel):
    topic_id: int
    topic_name: str

    class Config:
        from_attributes = True

