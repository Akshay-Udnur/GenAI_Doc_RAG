from pydantic import BaseModel, Field
from typing import Literal


class Conversation(BaseModel):
    type: Literal['human', 'ai']
    data: dict
    additional_kwargs:dict=Field(default={})
    example:bool=Field(default=False)
    
    
    
class ConversationHistory(BaseModel):
    history: list[Conversation] = Field(
        example=[
            {
                "type": "ai",
                "data": {'content':"Hello, I'm a comic book assistant. How can I help you today?"},
            },
            {"type": "human", "data": {'content':"tell me a quote from DC comics about life"}},
        ]
    )