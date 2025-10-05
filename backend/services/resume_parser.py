import PyPDF2
from docx import Document
import re
from typing import Dict, List, Any
from langdetect import detect
import html

class ResumeParser:
    def __init__(self):
        pass
    
    def _sanitize_text(self, text: str) -> str:
        """Sanitize text to prevent XSS and injection attacks"""
        if not text:
            return ""
        # Remove HTML tags and escape special characters
        text = re.sub(r'<[^>]+>', '', text)
        text = html.escape(text)
        # Limit length
        return text[:10000]
    
    def parse(self, content: bytes, filename: str) -> Dict[str, Any]:
        safe_filename = filename or "resume"
        
        text = self._extract_text(content, safe_filename)
        text = self._sanitize_text(text)
        language = self._detect_language(text)
        
        return {
            "raw_text": text[:5000],  # Limit raw text size
            "language": language,
            "name": self._sanitize_text(self._extract_name(text))[:100],
            "contact_info": self._extract_contact_info(text),
            "skills": [self._sanitize_text(skill)[:50] for skill in self._extract_skills(text)[:20]],
            "projects": self._extract_projects(text)[:10],
            "experience": self._extract_experience(text)[:10],
            "education": self._extract_education(text)[:5]
        }
    
    def _extract_text(self, content: bytes, filename: str) -> str:
        if filename.lower().endswith('.pdf'):
            return self._extract_pdf_text(content)
        elif filename.lower().endswith('.docx'):
            return self._extract_docx_text(content)
        else:
            raise ValueError("Unsupported file format")
    
    def _extract_pdf_text(self, content: bytes) -> str:
        from io import BytesIO
        pdf_reader = PyPDF2.PdfReader(BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    def _extract_docx_text(self, content: bytes) -> str:
        from io import BytesIO
        doc = Document(BytesIO(content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def _detect_language(self, text: str) -> str:
        try:
            return detect(text)
        except:
            return "en"
    
    def _extract_name(self, text: str) -> str:
        lines = text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 2 and len(line.split()) <= 4:
                if not any(char.isdigit() for char in line):
                    if not any(symbol in line for symbol in ['@', '.com', 'http', 'www']):
                        return line
        return ""
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        contact = {}
        
        # Email (with validation)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails and len(emails[0]) < 100:
            contact['email'] = self._sanitize_text(emails[0])
        
        # Phone (sanitized)
        phone_pattern = r'[\+]?[1-9]?[0-9]{7,15}'
        phones = re.findall(phone_pattern, text)
        if phones and len(phones[0]) < 20:
            contact['phone'] = re.sub(r'[^0-9+\-\s]', '', phones[0])
        
        # LinkedIn (validated)
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
        if linkedin and len(linkedin[0]) < 100:
            contact['linkedin'] = self._sanitize_text(linkedin[0])
        
        return contact
    
    def _extract_skills(self, text: str) -> List[str]:
        skills_section = self._find_section(text, ['skills', 'technical skills', 'competencies'])
        if not skills_section:
            return []
        
        # Common technical skills
        tech_skills = [
            'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'MongoDB',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Git', 'Linux',
            'Machine Learning', 'AI', 'Data Science', 'TensorFlow', 'PyTorch',
            'HTML', 'CSS', 'Angular', 'Vue.js', 'C++', 'C#', '.NET', 'Spring',
            'Django', 'Flask', 'PostgreSQL', 'MySQL', 'Redis', 'Elasticsearch'
        ]
        
        found_skills = []
        for skill in tech_skills:
            if skill.lower() in skills_section.lower():
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_projects(self, text: str) -> List[Dict[str, Any]]:
        projects_section = self._find_section(text, ['projects', 'project experience', 'personal projects'])
        if not projects_section:
            return []
        
        projects = []
        project_blocks = re.split(r'\n(?=[A-Z][^a-z]*[a-z])', projects_section)
        
        for block in project_blocks:
            if len(block.strip()) > 20:
                lines = block.strip().split('\n')
                title = lines[0].strip()
                description = ' '.join(lines[1:]).strip()
                
                technologies = self._extract_technologies(description)
                
                projects.append({
                    'title': title,
                    'description': description,
                    'technologies': technologies
                })
        
        return projects[:5]  # Limit to 5 projects
    
    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        exp_section = self._find_section(text, ['experience', 'work experience', 'employment'])
        if not exp_section:
            return []
        
        experiences = []
        exp_blocks = re.split(r'\n(?=[A-Z][^a-z]*[a-z])', exp_section)
        
        for block in exp_blocks:
            if len(block.strip()) > 20:
                lines = block.strip().split('\n')
                title = lines[0].strip()
                description = ' '.join(lines[1:]).strip()
                
                experiences.append({
                    'title': title,
                    'description': description
                })
        
        return experiences[:5]
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        edu_section = self._find_section(text, ['education', 'academic background'])
        if not edu_section:
            return []
        
        education = []
        edu_blocks = re.split(r'\n(?=[A-Z][^a-z]*[a-z])', edu_section)
        
        for block in edu_blocks:
            if len(block.strip()) > 10:
                lines = block.strip().split('\n')
                degree = lines[0].strip()
                institution = lines[1].strip() if len(lines) > 1 else ""
                
                education.append({
                    'degree': degree,
                    'institution': institution
                })
        
        return education[:3]
    
    def _find_section(self, text: str, keywords: List[str]) -> str:
        lines = text.split('\n')
        start_idx = -1
        
        for i, line in enumerate(lines):
            for keyword in keywords:
                if keyword.lower() in line.lower():
                    start_idx = i
                    break
            if start_idx != -1:
                break
        
        if start_idx == -1:
            return ""
        
        # Find next section or end
        end_idx = len(lines)
        section_keywords = ['experience', 'education', 'skills', 'projects', 'certifications']
        
        for i in range(start_idx + 1, len(lines)):
            line = lines[i].strip().lower()
            if any(keyword in line for keyword in section_keywords):
                if not any(kw in line for kw in keywords):
                    end_idx = i
                    break
        
        return '\n'.join(lines[start_idx:end_idx])
    
    def _extract_technologies(self, text: str) -> List[str]:
        tech_keywords = [
            'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'MongoDB',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'TensorFlow', 'PyTorch',
            'HTML', 'CSS', 'Angular', 'Vue.js', 'C++', 'C#', 'Django', 'Flask'
        ]
        
        found_tech = []
        for tech in tech_keywords:
            if tech.lower() in text.lower():
                found_tech.append(tech)
        
        return found_tech