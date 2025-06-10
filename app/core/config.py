import os
from datetime import timedelta


SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


CORS_ORIGINS = [
    "http://localhost:3000",
    "http://192.168.1.242:3000",
    "https://kanban-board-backend-3bfa.onrender.com"
]


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")


API_KEY = os.getenv("API_KEY", "FlowSpace")