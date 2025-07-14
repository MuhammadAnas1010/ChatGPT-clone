from pydantic import BaseModel
from typing import Literal


class new_chat_redis(BaseModel):
    sender: Literal['user', 'assistant']
    content: str