# Deployment Notes

## Backend Deployment (Hugging Face Spaces)

The backend should be deployed to Hugging Face Spaces with the following considerations:
- Make sure environment variables are properly configured
- Database connection should work with the hosted environment
- CORS is configured to allow all origins (adjust for production as needed)

## Frontend Deployment (Vercel)

When deploying the frontend to Vercel, ensure the following environment variable is set:

```
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.hf.space
```

### Steps to Configure Vercel Environment Variables:

1. Go to your Vercel dashboard
2. Select your frontend project
3. Navigate to Settings → Environment Variables
4. Add the following variable:
   - Key: `NEXT_PUBLIC_API_BASE_URL`
   - Value: Your backend URL (e.g., `https://maliaraees21-backend-deploy.hf.space`)

## Known Issues and Solutions

### 1. Bcrypt Password Length Limit
- Issue: Bcrypt has a 72-byte password length limit
- Solution: Passwords exceeding 72 bytes will be rejected with a clear error message
- Frontend should validate password length before sending to backend

### 2. CORS Configuration
- The backend currently allows all origins (`"*"`)
- For production, restrict this to specific frontend domains

### 3. Database Persistence
- Depending on hosting provider, ensure database persistence is configured properly
- Consider using a managed database service for production deployments