# AI Resume Analyzer & Role Fit System

## Project Overview
An AI-powered system that analyzes resumes and calculates their fit for specific roles using NLP and LLMs.

## Tech Stack
- **Backend:** Python, FastAPI, Motor (MongoDB async), Pydantic
- **Database:** MongoDB Atlas
- **AI/NLP:** OpenAI API, spaCy, PyMuPDF
- **Frontend:** React, Node.js (in separate module)

## Features List
- Resume parsing (PDF)
- AI-driven skill extraction and role matching
- User authentication (JWT)
- Role creation and management
- Fit score calculation

## Local Setup Instructions
1. Clone the repository
2. Backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
3. Frontend: (To be added)

## Environment Variable Setup
Copy `backend/.env.example` to `backend/.env` and update the values.

## Database Setup
1. Create a MongoDB Atlas cluster
2. Get the connection string and set it in `.env` as `MONGODB_URI`

## Deployment Steps
- **Backend:** Deploy to Render using `render.yaml`
- **Frontend:** Deploy to Vercel

## API Endpoint Documentation
Available at `http://localhost:8000/docs` (Swagger UI) when backend is running.

## Project Structure
- `/backend`: Python FastAPI application
- `/backend/app`: Core application code (routers, controllers, services, etc.)
- `/frontend`: React application (To be added)

## Future Improvements
- Multi-language support
- Batch resume processing
- Integration with ATS
