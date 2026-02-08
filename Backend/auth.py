# ============================================================
# auth.py — User Authentication Module (Signup / Login / JWT)
# ============================================================

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
import time

router = APIRouter()

# --- Configuration ---
SECRET_KEY = "supersecretkey"        # Replace with env variable in production
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Temporary in-memory user store (replace with DB later)
users_db = {}

# --- Pydantic Models ---
class User(BaseModel):
    email: str
    password: str

# --- Helper Functions ---
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def create_access_token(email: str):
    payload = {"sub": email, "iat": int(time.time())}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# --- Routes ---
@router.post("/signup")
def signup(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists.")
    users_db[user.email] = {"email": user.email, "password": hash_password(user.password)}
    return {"message": "User registered successfully!"}

@router.post("/login")
def login(user: User):
    stored_user = users_db.get(user.email)
    if not stored_user or not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
