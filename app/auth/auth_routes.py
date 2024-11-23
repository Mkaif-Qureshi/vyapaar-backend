from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from app.supabase_client import get_supabase_client
from app.auth.auth_handler import create_access_token
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
supabase = get_supabase_client()


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/signup")
def signup(full_name: str, email: str, password: str, role: str = "user"):
    hashed_password = hash_password(password)
    response = supabase.table("users").insert({
        "full_name": full_name,
        "email": email,
        "password_hash": hashed_password,
        "role": role
    }).execute()

    if response.error:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"msg": "User created successfully"}


@router.post("/login")
def login(email: str, password: str):
    response = supabase.table("users").select("*").eq("email", email).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user = response.data[0]
    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}
