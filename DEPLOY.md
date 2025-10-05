# Deployment Guide

## Vercel (Frontend)

1. Connect your GitHub repository to Vercel
2. Set build command: `cd frontend && npm run build`
3. Set output directory: `frontend/build`
4. Deploy automatically on push

## Railway (Backend)

1. Connect your GitHub repository to Railway
2. Railway will auto-detect Python and use `requirements.txt`
3. Set start command: `cd backend && python main.py`
4. Add environment variables if needed
5. Deploy automatically on push

## Environment Variables

### Backend (Railway)
- `PORT`: 8000 (default)
- `HOST`: 0.0.0.0 (default)

### Frontend (Vercel)
- `REACT_APP_API_URL`: Your Railway backend URL

## File Structure (Cleaned)

```
resume-analyzer/
├── backend/
│   ├── services/
│   ├── database/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── requirements.txt (for Railway)
├── vercel.json
├── railway.json
├── Procfile
└── .gitignore
```

## Removed Files

- Docker files (docker-compose.yml, Dockerfile)
- Batch files (*.bat)
- Test files
- Database files
- Duplicate files
- Deployment documentation

## Health Check

Backend includes `/health` endpoint for monitoring.