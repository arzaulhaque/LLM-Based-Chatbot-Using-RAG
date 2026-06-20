# LLM-Based-Chatbot-Using-RAG

## Backend Module 1 (Auth + Core Skeleton)

The backend skeleton follows a clean architecture-inspired layout under `backend/app`.

### Included in this module
- FastAPI app bootstrap with versioned routing (`/api/v1`)
- Core settings, logging, and exception handling
- SQLite-ready SQLAlchemy session/base setup
- Auth router with register/login/me/logout endpoints
- JWT and password hashing utilities
- User model + repository + auth use cases

### Quick start
```bash
cd backend
cp .env.example .env
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Auth endpoints
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/logout`
