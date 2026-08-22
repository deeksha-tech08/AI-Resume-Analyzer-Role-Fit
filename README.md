# AI Resume Analyzer & Role Fit System

## Project Overview
An intelligent, full-stack AI platform designed to analyze resumes against 30+ tech industry roles. The system extracts skills, calculates match percentages, evaluates section-by-section strength, and provides actionable insights for candidates using advanced NLP and Google's Gemini LLM.

## Tech Stack
- **Frontend:** React.js, Vite, Tailwind CSS
- **Backend:** Python, FastAPI, Motor (MongoDB async), Pydantic
- **Database:** MongoDB Atlas
- **AI/NLP:** Google Gemini API, spaCy, PyMuPDF

## Features List
- **Smart Role Discovery (30+ roles auto-analysis)**
- **Section Strength Analysis**
- **Role-wise Fit Score**
- Resume parsing (PDF)
- AI-driven skill extraction and role matching
- User authentication (JWT)

## Local Setup Instructions
1. Clone the repository
2. Backend:
   `ash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or env\Scripts\activate on Windows
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8001
   `
3. Frontend:
   `ash
   cd frontend
   npm install
   npm run dev -- --port 5174
   `

## Environment Variable Setup
Copy ackend/.env.example to ackend/.env and update the values.

## Database Setup
1. Create a MongoDB Atlas cluster
2. Get the connection string and set it in .env as MONGODB_URI

## Deployment Steps
- **Backend:** Deploy to Render using ender.yaml
- **Frontend:** Deploy to Vercel

## API Endpoint Documentation
Available at http://localhost:8001/docs (Swagger UI) when backend is running.

## Project Structure
- /backend: Python FastAPI application
- /backend/app: Core application code (routers, controllers, services, etc.)
- /frontend: React application

## Future Improvements
- Multi-language support
- Batch resume processing
- Integration with ATS
