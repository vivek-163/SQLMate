 
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class ChatMessage(BaseModel):
    username: str
    message: str
