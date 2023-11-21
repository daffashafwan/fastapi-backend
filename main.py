from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

class UserLogin(BaseModel):
    username: str
    password: str

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    port="dbport",
    user="dbuser",
    passwd="dbpassword",
    database="dbname"
)

@app.post("/login")
async def login(user: UserLogin):
    cursor = db.cursor()

    # Check if the user exists in the database
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (user.username, user.password))
    result = cursor.fetchone()

    if result:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")