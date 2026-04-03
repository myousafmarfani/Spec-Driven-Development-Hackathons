# Quickstart Guide: Full-Stack Todo Web Application

**Created**: 2026-02-08
**Feature**: Full-Stack Todo Web Application

## Overview

This guide provides a quick start to set up and run the Full-Stack Todo Web Application with Next.js frontend and FastAPI backend.

## Prerequisites

- Node.js 18+ installed
- Python 3.13+ installed
- PostgreSQL or access to Neon PostgreSQL database
- Git installed

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hackathon-todo-phase2
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
pip install uv  # if using uv as package manager
uv pip install -r requirements.txt
# OR with pip
pip install -r requirements.txt
```

#### Set Up Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
FRONTEND_URL=http://localhost:3000
```

#### Initialize the Database
```bash
# Run database migrations or initialization script
python -m backend.init_db
```

#### Run the Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
# OR
pnpm install
```

#### Set Up Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-openai-domain-key-for-phase-iii
```

#### Run the Frontend
```bash
cd frontend
npm run dev
# OR
pnpm dev
```

Frontend will be available at `http://localhost:3000`

## Running the Application

1. Start the backend: `cd backend && uvicorn main:app --reload --port 8000`
2. In a new terminal, start the frontend: `cd frontend && npm run dev`
3. Visit `http://localhost:3000` in your browser

## API Testing

Once running, you can test the API endpoints:

### Authentication
- Register: `POST http://localhost:8000/api/auth/signup`
- Login: `POST http://localhost:8000/api/auth/signin`

### Task Management (after authentication)
- Get tasks: `GET http://localhost:8000/api/{user_id}/tasks`
- Create task: `POST http://localhost:8000/api/{user_id}/tasks`
- Update task: `PUT http://localhost:8000/api/{user_id}/tasks/{task_id}`
- Delete task: `DELETE http://localhost:8000/api/{user_id}/tasks/{task_id}`
- Toggle completion: `PATCH http://localhost:8000/api/{user_id}/tasks/{task_id}/complete`

## Database Schema

The application uses PostgreSQL with two main tables:

1. **users** (managed by Better Auth):
   - id, email, name, password_hash, created_at, updated_at

2. **tasks**:
   - id, user_id (foreign key), title, description, completed, created_at, updated_at

Indexes are created on tasks.user_id, tasks.completed, and tasks.created_at for performance.

## Key Technologies

- **Frontend**: Next.js 16 with App Router, TypeScript, Tailwind CSS, Better Auth
- **Backend**: FastAPI, SQLModel, Pydantic, PostgreSQL
- **Authentication**: JWT tokens via Better Auth
- **Database**: Neon PostgreSQL (can use local PostgreSQL for development)

## Troubleshooting

### Common Issues
1. **Database connection errors**: Verify DATABASE_URL in backend .env
2. **Authentication not working**: Ensure BETTER_AUTH_SECRET is the same in both frontend and backend
3. **API calls failing**: Check that NEXT_PUBLIC_API_URL points to the correct backend URL
4. **CORS errors**: Ensure FRONTEND_URL in backend .env matches your frontend URL

### Environment Variable Matching
Make sure these values match between frontend and backend:
- BETTER_AUTH_SECRET should be identical in both .env files
- API URLs should be correctly configured