# Dashboard AI

A modern dashboard application with an integrated LLM Agent.

## Structure

- `frontend/`: Next.js application (Frontend)
- `backend/`: FastAPI application (Backend/Agent)

## Getting Started

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
pkill -9 -f uvicorn
source /opt/miniconda3/etc/profile.d/conda.sh
python -m uvicorn main:app --reload
```
