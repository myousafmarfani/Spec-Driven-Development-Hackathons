# Database Setup Instructions

## Neon PostgreSQL Setup

To set up the Neon PostgreSQL database for this project:

1. Go to https://neon.tech/
2. Create a new Neon account or sign in to your existing account
3. Create a new project
4. After project creation, copy the connection string from the project dashboard
5. Store the connection string in your backend/.env file as DATABASE_URL

Example connection string format:
```
DATABASE_URL=postgresql://username:password@ep-xxxxxxx.us-east-1.aws.neon.tech/neondb?sslmode=require
```

## Environment Configuration

Create a `.env` file in the backend directory with:
```
DATABASE_URL=your_neon_connection_string_here
BETTER_AUTH_SECRET=your_super_secret_jwt_key_here
FRONTEND_URL=http://localhost:3000
```