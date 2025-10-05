# Deployment Guide

## 🚀 Quick Deployment Options

### 1. GitHub Pages + Vercel (Free)

**Frontend (Vercel):**
```bash
# 1. Push to GitHub
git add .
git commit -m "Initial commit"
git push origin main

# 2. Connect to Vercel
# - Go to vercel.com
# - Import GitHub repository
# - Deploy frontend folder
```

**Backend (Railway/Render):**
```bash
# Railway.app (Recommended)
# 1. Connect GitHub repo
# 2. Select backend folder
# 3. Auto-deploys on push
```

### 2. Heroku (Full Stack)

```bash
# Install Heroku CLI
npm install -g heroku

# Login and create app
heroku login
heroku create your-resume-analyzer

# Deploy
git push heroku main
```

### 3. Docker Deployment

```bash
# Build and run
docker-compose up --build

# Production mode
docker-compose -f docker-compose.prod.yml up
```

### 4. VPS/Cloud Server

```bash
# Ubuntu/Debian setup
sudo apt update
sudo apt install python3 python3-pip nodejs npm

# Clone and setup
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer

# Backend
cd backend
pip3 install -r requirements.txt
python3 main.py &

# Frontend
cd ../frontend
npm install
npm run build
npm install -g serve
serve -s build -l 3000
```

## 🌐 Free Hosting Options

### Frontend Hosting
- **Vercel** (Recommended): vercel.com
- **Netlify**: netlify.com
- **GitHub Pages**: pages.github.com
- **Surge**: surge.sh

### Backend Hosting
- **Railway**: railway.app (Recommended)
- **Render**: render.com
- **Heroku**: heroku.com (Free tier limited)
- **PythonAnywhere**: pythonanywhere.com

### Full Stack Hosting
- **Heroku**: Full stack deployment
- **DigitalOcean App Platform**: $5/month
- **AWS Amplify**: Pay per use
- **Google Cloud Run**: Pay per use

## 📋 Environment Variables

Create `.env` files:

**Backend (.env):**
```
PORT=8000
CORS_ORIGINS=http://localhost:3000,https://your-frontend-url.com
```

**Frontend (.env):**
```
REACT_APP_API_URL=https://your-backend-url.com
```

## 🔧 Production Configuration

**Backend (main.py):**
```python
# Add for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Monitoring & Analytics

Add to your deployment:

```bash
# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Add logging
import logging
logging.basicConfig(level=logging.INFO)
```

## 🚀 CI/CD Pipeline

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Production
        run: |
          # Your deployment commands
```

## 📈 Scaling Options

1. **Database**: Add PostgreSQL/MongoDB
2. **Caching**: Redis for faster responses
3. **CDN**: CloudFlare for global distribution
4. **Load Balancer**: Multiple server instances

## 🔒 Security Checklist

- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] File upload limits set
- [ ] Rate limiting implemented
- [ ] Environment variables secured
- [ ] Dependencies updated

## 📞 Support

Need help deploying? Create an issue on GitHub!