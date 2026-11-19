# AI Resume Analyzer & Role Fit System

## Project Overview
An intelligent, full-stack AI platform designed to analyze resumes against 30+ tech industry roles. The system extracts skills, calculates match percentages, evaluates section-by-section strength, and provides actionable insights for candidates using advanced NLP and Google's Gemini LLM.

## Tech Stack
- **Frontend:** React.js, Vite, Tailwind CSS
- **Backend:** Python, FastAPI, Motor (MongoDB async), Pydantic
- **Database:** MongoDB Atlas
- **AI/NLP:** Google Gemini API, spaCy, PyMuPDF

## Features List
- **Smart Role Discovery (30+ roles auto-analysis)** — Upload your resume and instantly discover your Top 5 best-fit roles out of 30+.
- **Section Strength Analysis** — Granular scores for Skills, Experience, Education, Projects, and Achievements.
- **Role-wise Fit Score** — Detailed breakdown of matched skills, missing core skills, and optional skills for each role.
- **Resume Parsing (PDF)** — Advanced text extraction using PyMuPDF.
- **AI-driven Skill Extraction** — NLP-powered skill detection using spaCy.
- **AI Insights & Suggestions** — Powered by Google Gemini API for personalized improvement tips.
- **User Authentication (JWT)** — Secure login/register with httpOnly cookie-based sessions.
- **Analysis History** — Track and revisit all your past resume analyses.

## Local Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/deeksha-tech08/AI-Resume-Analyzer-Role-Fit.git
   cd AI-Resume-Analyzer-Role-Fit
   ```

2. Backend:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # macOS/Linux
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   uvicorn app.main:app --reload --port 8001
   ```

3. Frontend:
   ```bash
   cd frontend
   npm install
   npm run dev -- --port 5174
   ```

## Environment Variable Setup

Copy `backend/.env.example` to `backend/.env` and fill in the values:

```env
MONGODB_URI=your_mongodb_atlas_connection_string
JWT_SECRET=your_jwt_secret
GEMINI_API_KEY=your_gemini_api_key
```

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8001/api
```

## Database Setup
1. Create a MongoDB Atlas cluster
2. Whitelist your IP (or use `0.0.0.0/0` for development)
3. Get the connection string and set it in `.env` as `MONGODB_URI`

## Deployment Steps
- **Backend:** Deploy to Render using `render.yaml`
- **Frontend:** Deploy to Vercel

## API Endpoint Documentation
Available at [http://localhost:8001/docs](http://localhost:8001/docs) (Swagger UI) when the backend is running.

## Project Structure
```
├── backend/
│   ├── app/
│   │   ├── ai/              # AI engine (skill extraction, role matching, Gemini analyzer)
│   │   ├── controllers/     # Request handlers
│   │   ├── database/        # MongoDB connection
│   │   ├── middleware/       # Auth middleware
│   │   ├── models/          # Data models
│   │   ├── routers/         # API routes
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── utils/           # File parser, skill dictionary, validators
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── context/         # Auth context
│   │   ├── hooks/           # Custom React hooks
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service layer
│   │   └── utils/           # Helper functions
│   ├── package.json
│   └── .env.example
└── README.md
```

## Future Improvements
- Multi-language resume support
- Batch resume processing
- Direct ATS integration
- Resume improvement suggestions with before/after comparison
