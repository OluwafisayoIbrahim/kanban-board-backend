import uuid
from typing import Optional, Dict, Any
from app.db.supabase_client import supabase
from app.core.security import get_password_hash
from postgrest.exceptions import APIError

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email from Supabase"""
    try:
        response = supabase.table("users").select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]
        return None
    except APIError as e:
        print(f"Error getting user by email: {e}")
        return None

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Get user by username from Supabase"""
    try:
        response = supabase.table("users").select("*").eq("username", username).execute()
        if response.data:
            return response.data[0]
        return None
    except APIError as e:
        print(f"Error getting user by username: {e}")
        return None

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID from Supabase"""
    try:
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except APIError as e:
        print(f"Error getting user by ID: {e}")
        return None

def create_user(username: str, email: str, password: str) -> Optional[str]:
    """Create a new user in Supabase"""
    try:
        hashed = get_password_hash(password)
        user_id = str(uuid.uuid4())
        
        user_data = {
            "id": user_id,
            "username": username,
            "email": email,
            "hashed_password": hashed
        }
        
        response = supabase.table("users").insert(user_data).execute()
        
        if response.data:
            return user_id
        return None
        
    except APIError as e:
        print(f"Error creating user: {e}")
        return None

def update_user(user_id: str, update_data: Dict[str, Any]) -> bool:
    """Update user in Supabase"""
    try:
        response = supabase.table("users").update(update_data).eq("id", user_id).execute()
        return len(response.data) > 0
    except APIError as e:
        print(f"Error updating user: {e}")
        return False

def delete_user(user_id: str) -> bool:
    """Delete user from Supabase"""
    try:
        response = supabase.table("users").delete().eq("id", user_id).execute()
        return len(response.data) > 0
    except APIError as e:
        print(f"Error deleting user: {e}")
        return False