from fastapi import APIRouter, Depends, HTTPException
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/users", tags=["users"])
supabase = get_supabase_client()

@router.get("/")
def get_all_users():
    response = supabase.table("users").select("*").execute()
    if response.error:
        raise HTTPException(status_code=500, detail="Failed to fetch users")
    return response.data
