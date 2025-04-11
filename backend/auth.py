from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import bcrypt
import jwt
import os

# Secret Key for JWT
SECRET_KEY = "36b7e6ed81e23a9cba6c1fc1b076fe15789f2d98ac713eb297bf39c1e9c19d97"
ALGORITHM = "HS256"

# ✅ Dummy User Database
fake_users_db = {}

auth_router = APIRouter()

# ✅ User Schema
class User(BaseModel):
    username: str
    password: str

# ✅ Register Endpoint
@auth_router.post("/auth/register")
async def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    fake_users_db[user.username] = hashed_password
    return {"message": "Registration successful"}

# ✅ Login Endpoint
@auth_router.post("/auth/login")
async def login(user: User):
    if user.username not in fake_users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    stored_hashed_password = fake_users_db[user.username]
    if not bcrypt.checkpw(user.password.encode('utf-8'), stored_hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"username": user.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}


