from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Simple in-memory user store for testing
USERS_DB: Dict[str, str] = {
    "testuser": "password123",
    "admin": "admin123"
}


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    username: str
    token: str


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Login API"}


@app.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(credentials: LoginRequest):
    """
    Simple login endpoint that validates username and password.
    Returns a token on successful authentication.
    """
    # Check if user exists
    if credentials.username not in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Verify password
    if USERS_DB[credentials.username] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Generate a simple token (in production, use JWT)
    token = f"token_{credentials.username}_authenticated"

    return LoginResponse(
        message="Login successful",
        username=credentials.username,
        token=token
    )
