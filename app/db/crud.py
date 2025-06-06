import uuid
from typing import Optional, Dict, Any
from app.db.supabase_client import supabase
from app.core.security import get_password_hash
from postgrest.exceptions import APIError
from datetime import datetime, timedelta
import datetime as dt

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
def add_token_to_blacklist(token: str, expires_minutes: int = 30) -> bool:
    """Add token to blacklist"""
    try:
        expires_at = datetime.now(dt.timezone.utc) + timedelta(minutes=expires_minutes)
        
        blacklist_data = {
            "token": token,
            "expires_at": expires_at.isoformat()
        }
        
        response = supabase.table("token_blacklist").insert(blacklist_data).execute()
        return len(response.data) > 0
    except APIError as e:
        print(f"Error adding token to blacklist: {e}")
        return False

def is_token_blacklisted(token: str) -> bool:
    """Check if token is blacklisted"""
    try:
        now = datetime.now(dt.timezone.utc).isoformat()
        
        response = supabase.table("token_blacklist")\
            .select("token")\
            .eq("token", token)\
            .gt("expires_at", now)\
            .execute()
        
        return len(response.data) > 0
    except APIError as e:
        print(f"Error checking token blacklist: {e}")
        return False

def cleanup_expired_tokens() -> bool:
    """Remove expired tokens from blacklist"""
    try:
        now = datetime.now(dt.timezone.utc).isoformat()
        
        response = supabase.table("token_blacklist")\
            .delete()\
            .lt("expires_at", now)\
            .execute()
        
        print(f"Cleaned up {len(response.data)} expired tokens")
        return True
    except APIError as e:
        print(f"Error cleaning up expired tokens: {e}")
        return False