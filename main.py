from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    username: str
    token: str


@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    if request.username == "admin" and request.password == "admin123":
        return LoginResponse(
            message="Login successful",
            username=request.username,
            token="fake-jwt-token-123"
        )
    raise HTTPException(status_code=401, detail="Invalid credentials")
