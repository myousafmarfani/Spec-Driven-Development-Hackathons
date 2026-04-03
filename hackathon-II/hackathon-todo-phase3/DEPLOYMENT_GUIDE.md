# Deployment Guide for Todo Application

This guide provides instructions for deploying the full-stack todo application to production environments.

## Prerequisites

- Git repository ready
- Accounts on chosen hosting platforms (Vercel for frontend, Railway/Vercel for backend)
- Domain names configured (if using custom domains)
- SSL certificates (if required)

## Backend Deployment

### Option 1: Railway

1. Create a Railway account at https://railway.app/
2. Connect your GitHub repository to Railway
3. Create a new project and select your repository
4. Configure the following environment variables in Railway:
   - `DATABASE_URL`: PostgreSQL connection string for your production database
   - `BETTER_AUTH_SECRET`: A strong secret key for JWT signing
   - `FRONTEND_URL`: The URL of your deployed frontend (e.g., https://your-frontend.vercel.app)
   - `LOG_LEVEL`: Set to INFO or DEBUG

5. In the Railway settings, set the deployment command:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`

6. Deploy and take note of the deployment URL

### Option 2: Vercel

1. Create a Vercel account at https://vercel.com/
2. Import your project from GitHub
3. Configure the project settings:
   - Framework Preset: Other
   - Build Command: `pip install -r requirements.txt && python -m your_build_script`
   - Output Directory: Leave empty for API deployments
   - Install Command: Leave empty or specify if needed

4. Add the required environment variables:
   - `DATABASE_URL`
   - `BETTER_AUTH_SECRET`
   - `FRONTEND_URL`
   - `LOG_LEVEL`

5. Add a Procfile or specify the start command:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

## Frontend Deployment

### Vercel (Recommended)

1. Create a Vercel account at https://vercel.com/
2. Import your frontend repository
3. In the project settings:
   - Framework Preset: Next.js
   - Build Command: `npm run build` (or `pnpm build` if using pnpm)
   - Output Directory: `out` (for static export) or leave empty for server-side rendering

4. Add the following environment variables:
   - `NEXT_PUBLIC_API_URL`: The URL of your deployed backend API
   - `NEXT_PUBLIC_BETTER_AUTH_SECRET`: Same secret as backend for authentication
   - `NODE_ENV`: production

5. Under "Build & Development Settings":
   - Select "Automatically detect project settings"

6. Deploy the frontend

## Configuration

### Environment Variables Mapping

After deployment, ensure these environment variables are consistent between frontend and backend:

- `BETTER_AUTH_SECRET` (Backend) should match `NEXT_PUBLIC_BETTER_AUTH_SECRET` (Frontend) for authentication to work
- `FRONTEND_URL` in backend should match the actual frontend deployment URL
- `NEXT_PUBLIC_API_URL` in frontend should match the actual backend deployment URL

### CORS Configuration

The backend should have CORS configured to allow requests from your frontend domain:
- Production frontend URL (e.g., https://your-app.vercel.app)
- If you have other allowed origins, add them as needed

## Database Migration

If you're using a new database for production:

1. Run your database initialization script in production
2. For SQLModel/SQLAlchemy apps, you might need to run alembic migrations:
   ```bash
   alembic upgrade head
   ```

3. For Neon PostgreSQL, you can run this in a deploy hook or manually after deployment

## Post-Deployment Verification

After both frontend and backend are deployed:

1. Verify the backend health endpoint: `https://your-backend-domain.com/health`
2. Check API documentation: `https://your-backend-domain.com/docs`
3. Visit the frontend and test:
   - Sign up functionality
   - Sign in functionality
   - Task creation, viewing, updating, and deletion
   - Task completion toggling
   - Sign out functionality

## Common Issues & Troubleshooting

### CORS Errors
- Ensure `FRONTEND_URL` in backend matches exactly with the deployed frontend URL
- Check for trailing slashes or protocol mismatches

### Authentication Failures
- Verify that `BETTER_AUTH_SECRET` is identical in both frontend and backend
- Ensure JWT tokens are being sent properly with API requests

### Database Connection Issues
- Confirm the `DATABASE_URL` is correctly configured
- Check that the database service is running and accessible
- Verify the database user has appropriate permissions

### API Connection Failures
- Verify that `NEXT_PUBLIC_API_URL` points to the correct backend URL
- Ensure the backend is deployed and accessible
- Check that the backend is configured to accept requests from the frontend domain

## Scaling Considerations

### Backend
- Consider using a managed database service (Neon, Supabase, AWS RDS, etc.)
- Implement caching for frequently accessed data
- Use a load balancer if expecting high traffic
- Set up monitoring and alerting

### Frontend
- Leverage CDN for asset delivery
- Implement proper caching strategies
- Consider internationalization if needed
- Optimize bundle size

## Monitoring and Maintenance

### Logs
- Set up centralized logging for both frontend and backend
- Monitor error rates and performance metrics
- Set up alerts for critical failures

### Backups
- Regularly backup your database
- Store backups in secure, redundant locations
- Test restoration procedures periodically

### Security
- Regularly update dependencies
- Implement rate limiting to prevent abuse
- Monitor for suspicious activities
- Use HTTPS for all communications