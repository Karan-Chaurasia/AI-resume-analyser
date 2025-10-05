# AI Resume Analyser

🚀 **AI-Powered Resume Analysis with ATS Integration**

Comprehensive resume analyser with multilingual support, job matching, and ATS compatibility scoring.

## ✨ Features

- **AI-Powered Analysis**: Advanced skill extraction and job matching
- **ATS Integration**: Applicant Tracking System compatibility scoring
- **Multilingual Support**: Analyses resumes in 21+ languages
- **Contact Detection**: Accurate LinkedIn/GitHub link extraction
- **Project Analysis**: Detailed project and technology extraction
- **Improvement Suggestions**: Personalized recommendations

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
docker-compose up
```
Access at: http://localhost:3000

### Option 2: Manual Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

## 📋 Requirements

- Python 3.8+
- Node.js 16+
- Docker (optional)

## 🔧 Installation

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Run Application**
```bash
# Backend (Terminal 1)
cd backend && python main.py

# Frontend (Terminal 2)  
cd frontend && npm start
```

## 🌐 Live Demo

Try it live: [Resume Analyser Demo](https://your-deployed-url.com)

## 📖 API Documentation

### Analyse Resume
```bash
POST /api/analyse-resume
Content-Type: multipart/form-data

curl -X POST -F "file=@resume.pdf" http://localhost:8000/api/analyse-resume
```

### Response Format
```json
{
  "extracted_data": {
    "name": "John Doe",
    "skills": ["Python", "React", "AWS"],
    "contact_info": {
      "email": "john@example.com",
      "linkedin": "https://linkedin.com/in/johndoe"
    }
  },
  "ats_analysis": {
    "ats_score": 85,
    "ats_friendly": true,
    "compatibility_rating": "Excellent"
  },
  "job_matches": [...],
  "suggestions": [...]
}
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python, AI/ML
- **Frontend**: React, TypeScript
- **AI**: Custom HR analyser with 200+ skill database
- **ATS**: Integrated compatibility scoring
- **Languages**: Supports 21+ languages

## 📁 Project Structure

```
resume-analyzer/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── ai_hr_analyzer.py    # AI HR analysis
│   ├── ats_analyzer.py      # ATS compatibility
│   ├── translator.py        # Multilingual support
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/                 # React application
│   ├── package.json         # Node dependencies
│   └── public/              # Static files
├── docker-compose.yml       # Docker setup
└── README.md               # This file
```

## 🚀 Deployment Options

### Heroku
```bash
# Install Heroku CLI
heroku create your-app-name
git push heroku main
```

### Vercel (Frontend)
```bash
# Install Vercel CLI
cd frontend
vercel --prod
```

### Railway
```bash
# Connect GitHub repo to Railway
# Auto-deploys on push
```

### Docker
```bash
docker build -t resume-analyser .
docker run -p 3000:3000 resume-analyser
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🆘 Support

- 📧 Email: support@resumeanalyser.com
- 💬 Issues: [GitHub Issues](https://github.com/yourusername/resume-analyser/issues)
- 📖 Docs: [Documentation](https://docs.resumeanalyser.com)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/resume-analyser&type=Date)](https://star-history.com/#yourusername/resume-analyser&Date)

---

**Made with ❤️ for job seekers worldwide**