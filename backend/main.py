from fastapi import FastAPI, HTTPException, Depends
from backend.auth import auth_router  # Import authentication routes
import mysql.connector
from pydantic import BaseModel

# FastAPI app
app = FastAPI()

# Include authentication routes
app.include_router(auth_router)

# Database connection function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Change if your MySQL runs elsewhere
            user="your_mysql_user",  
            password="your_mysql_password",
            database="your_database"
        )
        return conn
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

# Query model
class QueryRequest(BaseModel):
    query: str

# Chat API to fetch data from MySQL
@app.post("/chat")
def chat_with_db(request: QueryRequest):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(request.query)
        result = cursor.fetchall()

        return {"status": "success", "data": result}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"MySQL Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Query: {e}")
    finally:
        cursor.close()
        conn.close()

