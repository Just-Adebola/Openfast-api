from fastapi import FastAPI, status, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
import time
from uuid import uuid4

app = FastAPI()

# Middleware to track process time


@app.middleware("http")
async def process_time(request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter()
    duration = end_time - start_time
    response.headers["X-Process-Time"] = str(duration)
    print(duration)
    return response

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["(http://127.0.0.1:8000)"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User Model


class User(BaseModel):
    id: str = None
    first_name: str
    last_name: str
    age: int
    email: str
    height: float


# In-memory user storage
my_users = []

# to create a new user


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()],
    age: Annotated[int, Form()],
    email: Annotated[str, Form()],
    height: Annotated[float, Form()],
):
    try:
        # Generate UUID for user ID
        user_id = str(uuid4())
        new_user = User(
            id=user_id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            email=email,
            height=height,
        )
        my_users.append(new_user)
        return {"message": "Successfully created."}
    except Exception as e:
        return {"error": str(e)}
