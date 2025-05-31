from datetime import timedelta

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

CORS_ORIGINS = [
    "http://localhost:3000",
    "https://kanban-board-backend-3bfa.onrender.com"
]
