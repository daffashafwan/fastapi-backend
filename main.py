from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg

app = FastAPI()

class UserLogin(BaseModel):
    username: str
    password: str

# Function to create a connection pool
async def create_connection_pool():
    return await asyncpg.create_pool(
        user='daffashafwan',
        password='',
        database='appdb',
        host='localhost'
    )

@app.on_event("startup")
async def startup():
    app.state.pool = await create_connection_pool()

@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()

@app.post("/login")
async def login(user: UserLogin):
    query = "SELECT * FROM users WHERE username = $1 AND password = $2"
    async with app.state.pool.acquire() as connection:
        result = await connection.fetchrow(query, user.username, user.password)
        if result:
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")