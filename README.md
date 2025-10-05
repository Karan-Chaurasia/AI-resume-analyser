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

### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

Access at: http://localhost:3000

### Cloud Deployment

**Backend (Render):**
- Connect GitHub repo to Render
- Uses `render.yaml` configuration
- Auto-deploys on push

**Frontend (Vercel):**
- Connect GitHub repo to Vercel
- Uses `vercel.json` configuration
- Auto-deploys on push

## 📋 Requirements

- Python 3.8+
- Node.js 16+

## 🔧 Installation

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

2. **Setup Virtual Environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
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

## 📖 API Documentation

### Analyse Resume
```bash
POST /api/analyse-resume
Content-Type: multipart/form-data

curl -X POST -F "file=@resume.pdf" http://localhost:8000/api/analyse-resume
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
└── README.md               # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

**Made with ❤️ for job seekers worldwide**