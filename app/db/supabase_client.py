import os
from supabase import create_client, Client
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def validate_supabase_config():
    """Validate Supabase configuration"""
    if not SUPABASE_URL:
        raise ValueError(
            "SUPABASE_URL environment variable is not set. "
            "Please add it to your .env file: SUPABASE_URL=https://your-project.supabase.co"
        )
    
    if not SUPABASE_ANON_KEY:
        raise ValueError(
            "SUPABASE_ANON_KEY environment variable is not set. "
            "Please add it to your .env file with your project's anon key."
        )
    
    if SUPABASE_URL == "your-supabase-url" or "your-project" in SUPABASE_URL:
        raise ValueError(
            "SUPABASE_URL contains placeholder text. "
            "Please replace with your actual Supabase project URL from the dashboard."
        )
    
    if not SUPABASE_URL.startswith("https://"):
        raise ValueError(
            f"SUPABASE_URL must start with 'https://'. Got: {SUPABASE_URL}"
        )

def get_supabase_client() -> Client:
    """Get Supabase client instance with validation"""
    validate_supabase_config()
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

try:
    supabase: Client = get_supabase_client()
    print("✅ Supabase client initialized successfully")
except Exception as e:
    print(f"❌ Supabase initialization failed: {e}")
    print("\n🔧 To fix this:")
    print("1. Go to your Supabase dashboard: https://supabase.com/dashboard")
    print("2. Select your project")
    print("3. Go to Settings → API")
    print("4. Copy your Project URL and anon/public key")
    print("5. Add them to your .env file")
    raise