 
from fastapi import APIRouter, HTTPException
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()
chat_db = {}  # Temporary storage for chat history

class ChatMessage(BaseModel):
    username: str
    message: str

@router.post("/save")
def save_chat(chat: ChatMessage):
    if chat.username not in chat_db:
        chat_db[chat.username] = []
    chat_db[chat.username].append({"timestamp": datetime.utcnow(), "message": chat.message})
    return {"message": "Chat saved successfully"}

@router.get("/history/{username}")
def get_chat_history(username: str):
    if username not in chat_db:
        raise HTTPException(status_code=404, detail="No chat history found")
    return chat_db[username]
