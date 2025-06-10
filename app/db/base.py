import os
from supabase import create_client, Client
from typing import Optional

SUPABASE_URL = os.getenv("SUPABASE_URL", "your-supabase-url")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "your-supabase-anon-key")

def init_db():
    """
    Initialize database connection and verify table exists.
    Note: Table should be created via Supabase dashboard or SQL editor.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("users").select("count", count="exact").limit(1).execute()
        print(f"✅ Supabase connection successful. Users table exists.")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        print("Make sure to:")
        print("1. Set SUPABASE_URL and SUPABASE_ANON_KEY environment variables")
        print("2. Create the 'users' table in your Supabase dashboard")
        return False

def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_connection():
    """Legacy function name - returns Supabase client instead of SQLite connection"""
    return get_supabase_client()