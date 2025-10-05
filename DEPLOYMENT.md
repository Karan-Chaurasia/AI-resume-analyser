# Resume Analyzer Deployment Guide

## Local Development

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Setup
1. Clone the repository
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start the development server:
   ```bash
   npm start
   ```
5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Vercel Deployment

### Prerequisites
- GitHub account
- Vercel account (free tier available)

### Steps
1. **Push to GitHub:**
   - Create a new repository on GitHub
   - Push your code to the repository:
     ```bash
     git add .
     git commit -m "Initial commit"
     git push origin main
     ```

2. **Deploy to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign in with your GitHub account
   - Click "New Project"
   - Import your resume-analyzer repository
   - Configure the project:
     - Framework Preset: Create React App
     - Root Directory: `frontend`
     - Build Command: `npm run build`
     - Output Directory: `build`
   - Add environment variables:
     - `REACT_APP_API_URL`: Your backend API URL
   - Click "Deploy"

3. **Update Backend URL:**
   - After deployment, update the `REACT_APP_API_URL` in your Vercel project settings
   - Or update the `.env.production` file with your actual backend URL

### Environment Variables
- **Development:** Uses `http://localhost:8000` (from `.env`)
- **Production:** Uses the URL from `REACT_APP_API_URL` environment variable

## Backend Deployment
Make sure your backend is deployed and accessible. Popular options:
- Heroku
- Railway
- Render
- AWS/GCP/Azure

Update the `REACT_APP_API_URL` in your Vercel environment variables to point to your deployed backend.