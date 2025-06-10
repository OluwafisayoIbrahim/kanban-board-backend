import os
from supabase import create_client, Client
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

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

def validate_service_role_config():
    """Validate service role configuration for admin operations"""
    if not SUPABASE_SERVICE_ROLE_KEY:
        print("⚠️  SUPABASE_SERVICE_ROLE_KEY not found. Admin operations (like file uploads) may fail due to RLS policies.")
        return False
    
    if "your-service-role" in SUPABASE_SERVICE_ROLE_KEY:
        print("⚠️  SUPABASE_SERVICE_ROLE_KEY contains placeholder text.")
        return False
    
    return True

def get_supabase_client() -> Client:
    """Get Supabase client instance with validation"""
    validate_supabase_config()
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_supabase_admin_client() -> Optional[Client]:
    """Get Supabase admin client for operations that need to bypass RLS"""
    validate_supabase_config()
    
    if not validate_service_role_config():
        return None
    
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

try:
    # Regular client for user operations
    supabase: Client = get_supabase_client()
    print("✅ Supabase client initialized successfully")
    
    # Admin client for storage operations (bypasses RLS)
    supabase_admin: Optional[Client] = get_supabase_admin_client()
    if supabase_admin:
        print("✅ Supabase admin client initialized successfully")
    else:
        print("⚠️  Supabase admin client not available - add SUPABASE_SERVICE_ROLE_KEY to .env")
        
except Exception as e:
    print(f"❌ Supabase initialization failed: {e}")
    print("\n🔧 To fix this:")
    print("1. Go to your Supabase dashboard: https://supabase.com/dashboard")
    print("2. Select your project")
    print("3. Go to Settings → API")
    print("4. Copy your Project URL and anon/public key")
    print("5. For file uploads, also copy the service_role key")
    print("6. Add them to your .env file:")
    print("   SUPABASE_URL=your-project-url")
    print("   SUPABASE_ANON_KEY=your-anon-key")
    print("   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key")
    raise