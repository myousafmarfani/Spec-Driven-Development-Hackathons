# Hackathon Todo App - Phase II

A full-stack todo application with user authentication and task management built using Next.js 16, FastAPI, and Neon PostgreSQL.

## Project Overview

This project implements a comprehensive todo application with user authentication, task management, and real-time updates. It follows a monorepo structure with clear separation of concerns between frontend and backend services.

### Features

- **User Authentication**: JWT-based authentication with registration and login
- **Task Management**: Create, read, update, delete, and mark tasks as complete/incomplete
- **Secure API**: Protected endpoints with proper authentication
- **Responsive UI**: Mobile-first design with responsive components
- **Data Isolation**: Users can only access their own tasks

### Tech Stack

#### Frontend
- Next.js 16 (App Router)
- React 19+
- TypeScript
- Tailwind CSS
- Better Auth
- SWR for data fetching

#### Backend
- Python 3.13+
- FastAPI
- SQLModel
- Pydantic
- PostgreSQL (Neon)

#### Infrastructure
- Docker & Docker Compose
- Environment-based configurations

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.13+
- Docker and Docker Compose
- Git

### Environment Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd hackathon-todo-phase2
```

2. Set up backend:
```bash
cd backend
pip install -e .
# or if using uv:
uv pip install -e .
```

3. Set up frontend:
```bash
cd frontend
npm install
# or
pnpm install
```

### Configuration

#### Backend Configuration

1. Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your_super_secret_jwt_key_here
FRONTEND_URL=http://localhost:3000
LOG_LEVEL=INFO
```

2. Set up Neon PostgreSQL database (or use local PostgreSQL for development)

#### Frontend Configuration

1. Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_SECRET=your_super_secret_jwt_key_here
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_openai_domain_key_for_phase_iii
```

### Running the Application

#### Development Mode

1. Start the backend:
```bash
cd backend
uvicorn main:app --reload
```

2. In a new terminal, start the frontend:
```bash
cd frontend
npm run dev
# or
pnpm dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Documentation: http://localhost:8000/docs

#### Using Docker

Alternatively, you can run the entire application using Docker Compose:

```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Documentation: http://localhost:8000/docs

For production deployments, ensure you update the environment variables in the `docker-compose.yml` file with strong, production-grade secrets.

To run in detached mode:
```bash
docker-compose up --build -d
```

To stop the containers:
```bash
docker-compose down
```

## Project Structure

```
hackathon-todo-phase2/
├── backend/                 # FastAPI backend application
│   ├── models.py           # SQLModel database models
│   ├── db.py              # Database connection layer
│   ├── auth.py            # JWT authentication logic
│   ├── schemas.py         # Pydantic schemas
│   ├── routes/
│   │   └── tasks.py       # Task-related API endpoints
│   ├── main.py            # FastAPI application entry point
│   ├── init_db.py         # Database initialization script
│   └── pyproject.toml     # Python dependencies
├── frontend/               # Next.js frontend application
│   ├── app/               # App Router pages
│   │   ├── auth/          # Authentication pages
│   │   │   ├── signin/
│   │   │   └── signup/
│   │   └── tasks/         # Tasks page
│   ├── components/        # Reusable UI components
│   │   └── tasks/         # Task-specific components
│   ├── lib/               # Utility functions
│   │   ├── auth.ts        # Authentication helpers
│   │   ├── api.ts         # API client wrapper
│   │   └── types.ts       # TypeScript type definitions
│   ├── package.json       # Frontend dependencies
│   └── .env.local         # Frontend environment variables
├── docker-compose.yml      # Docker configuration
├── .env                   # Environment variables template
└── README.md              # This file
```

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/signin` - Authenticate a user

### Task Management (All require JWT token)

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion

## Development

### Adding New Features

1. Create feature specifications in the `specs/` directory
2. Generate implementation plan: `sp.plan`
3. Generate tasks: `sp.tasks`
4. Implement features: `sp.implement`

### Testing

#### Backend Tests
```bash
cd backend
pytest
```

#### Frontend Tests
```bash
cd frontend
npm test
```

#### End-to-End Tests
Run the end-to-end test script:
```bash
python test_e2e.py
```

## Deployment

### Backend Deployment

1. Set up environment variables for production
2. Deploy using your preferred platform (Railway, Vercel, Render, etc.)
3. Ensure the database connection is configured properly

### Frontend Deployment

1. Build the application: `npm run build`
2. Deploy to Vercel, Netlify, or your preferred hosting platform
3. Configure environment variables

### Environment Variables for Production

#### Backend
- `DATABASE_URL` - PostgreSQL database connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT signing
- `FRONTEND_URL` - URL of the frontend application for CORS

#### Frontend
- `NEXT_PUBLIC_API_URL` - URL of the backend API
- `NEXT_PUBLIC_BETTER_AUTH_SECRET` - Secret key for authentication (if needed)

## Security

- JWT tokens for authentication
- User data isolation (users can only access their own tasks)
- Input validation on all endpoints
- Parameterized queries to prevent SQL injection
- CORS configured to only allow trusted origins

## Troubleshooting

### Common Issues

1. **Database Connection**: Ensure your `DATABASE_URL` is correctly configured
2. **Authentication**: Verify that `BETTER_AUTH_SECRET` is the same in both frontend and backend
3. **API Calls**: Check that `NEXT_PUBLIC_API_URL` points to the correct backend URL
4. **CORS Errors**: Ensure `FRONTEND_URL` in backend `.env` matches your frontend URL

### Debugging Tips

- Enable DEBUG logging in the backend for detailed request/response logs
- Check browser developer tools for frontend errors
- Verify that both frontend and backend are running simultaneously during development

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.