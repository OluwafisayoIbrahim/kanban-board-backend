# 🔐 FastAPI API for FlowSpace Kanban board
This is a simple authentication API built with **FastAPI**, featuring:

- User Sign Up
- User Sign In
- Get Authenticated User Info
- API Key Authentication for all endpoints
- Swagger/OpenAPI documentation

---

## 📁 Project Structure

```
.
├── app
│   ├── main.py
│   ├── auth.py
│   ├── dependencies.py
│   └── models.py
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/fastapi-auth-api.git
cd fastapi-auth-api
```

### 2. Create virtual environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Run the App

```bash
uvicorn app.main:app --reload
```

API Docs available at:
🔗 http://127.0.0.1:8000/docs

## 🔐 API Key Authentication

All endpoints require an API key passed via the request header:

```
Header Key:     x-api-key
Header Value:   API_KEY
```

Example cURL request:

```bash
curl -X 'POST' \
  'http://localhost:8000/auth/signup' \
  -H 'accept: application/json' \
  -H 'x-api-key: API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword"
}'
```

## 📦 Endpoints Summary

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/signup` | Register new user | ✅ Yes |
| POST | `/auth/signin` | Login user | ✅ Yes |
| GET | `/auth/me` | Get current user | ✅ Yes |
