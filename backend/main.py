from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional
import PyPDF2
from docx import Document
import re
from langdetect import detect
import io
import os
from translator import translate_text, translate_to_english, TRANSLATIONS
from ai_hr_analyser import AIHRAnalyser
from ats_analyser import ATSAnalyser

app = FastAPI(title="Resume Analyser API", version="1.0.0")

# Cache analyser instances for better performance
hr_analyser_instance = AIHRAnalyser()
ats_analyser_instance = ATSAnalyser()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text(content: bytes, filename: str) -> str:
    text = ""
    try:
        if filename.lower().endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        elif filename.lower().endswith('.docx'):
            doc = Document(io.BytesIO(content))
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n"
    except (PyPDF2.errors.PdfReadError, ValueError, IOError) as e:
        return "Error extracting text: Unable to process file"
    except Exception:
        return "Error extracting text: Unknown error occurred"
    
    return text.strip() if text.strip() else "No text found"

def ai_analyse_resume(resume_text: str, language: str = "en") -> dict:
    """AI-powered comprehensive resume analysis"""
    
    analysis = {
        "name": extract_name_ai(resume_text),
        "contact": extract_contact_ai(resume_text),
        "skills": extract_skills_ai(resume_text, language),
        "experience": extract_experience_ai(resume_text, language),
        "projects": extract_projects_ai(resume_text, language),
        "education": extract_education_ai(resume_text, language),
        "strengths": analyse_strengths_ai(resume_text, language),
        "weaknesses": analyse_weaknesses_ai(resume_text, language),
        "suggestions": generate_suggestions_ai(resume_text, language)
    }
    
    return analysis

def extract_name_ai(text: str) -> str:
    """AI-enhanced name extraction"""
    lines = text.split('\n')
    
    name_patterns = [
        r'^[A-Z][a-z]+ [A-Z][a-z]+',
        r'^[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+',
        r'^[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+',
    ]
    
    for line in lines[:10]:
        line = line.strip()
        if 2 < len(line) < 50 and not '@' in line and not re.search(r'\d{3,}', line):
            for pattern in name_patterns:
                if re.match(pattern, line):
                    return line
            if not any(word.lower() in ['resume', 'cv', 'curriculum', 'profile'] for word in line.split()):
                return line
    
    return "Unknown"

def extract_contact_ai(text: str) -> dict:
    """Enhanced contact extraction"""
    contact = {}
    
    email_patterns = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        r'email[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
        r'e-mail[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'
    ]
    
    for pattern in email_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            contact['email'] = match.group(1) if match.groups() else match.group()
            break
    
    phone_patterns = [
        r'(\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9})',
        r'(\(\d{3}\)\s?\d{3}[-.\s]?\d{4})',
        r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',
        r'phone[:\s]*(\+?\d[\d\s\-\(\)]{7,})'
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            contact['phone'] = match.group(1)
            break
    
    # Aggressive LinkedIn detection - finds any LinkedIn reference
    linkedin_patterns = [
        # Any LinkedIn URL format
        r'(?:https?://)?(?:www\.)?linkedin\.com/in/([^\s\)\]\|;,]+)',
        r'(?:https?://)?(?:www\.)?linkedin\.com/pub/([^\s\)\]\|;,]+)',
        r'(?:https?://)?(?:www\.)?linkedin\.com/profile/([^\s\)\]\|;,]+)',
        # LinkedIn anywhere in text
        r'linkedin\.com/in/([^\s\)\]\|;,]+)',
        r'linkedin\.com/pub/([^\s\)\]\|;,]+)',
        # LinkedIn with any separator
        r'(?:linkedin|LinkedIn|LINKEDIN)\s*[:\-/|\s]*([a-zA-Z][a-zA-Z0-9._-]{2,50})',
        # Any line containing linkedin
        r'.*linkedin.*?([a-zA-Z][a-zA-Z0-9._-]{3,30}).*',
        # Standalone usernames near linkedin
        r'([a-zA-Z][a-zA-Z0-9._-]{3,30}).*linkedin',
        r'linkedin.*?([a-zA-Z][a-zA-Z0-9._-]{3,30})',
        # Simple patterns
        r'(?:^|\s)([a-zA-Z][a-zA-Z0-9._-]{3,30})(?=.*linkedin)',
        r'(?:linkedin)(?:[^a-zA-Z0-9]*?)([a-zA-Z][a-zA-Z0-9._-]{3,30})'
    ]
    
    # Try each pattern and take first valid match
    for pattern in linkedin_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            username = match.strip().rstrip('/')
            # Minimal validation - just check it's reasonable
            if (username and 
                len(username) >= 3 and len(username) <= 50 and
                username[0].isalpha() and
                not username.lower() in ['linkedin', 'github', 'twitter', 'facebook'] and
                not username.startswith(('http', 'www')) and
                not username.endswith(('.com', '.net', '.org'))):
                contact['linkedin'] = f"https://linkedin.com/in/{username}"
                break
        if 'linkedin' in contact:
            break
    
    # Aggressive GitHub detection - finds any GitHub reference
    github_patterns = [
        # Any GitHub URL format
        r'(?:https?://)?(?:www\.)?github\.com/([^\s\)\]\|;,]+)',
        r'(?:https?://)?([^\s\)\]\|;,]+)\.github\.io',
        # GitHub anywhere in text
        r'github\.com/([^\s\)\]\|;,]+)',
        # GitHub with any separator
        r'(?:github|GitHub|GITHUB)\s*[:\-/|\s]*([a-zA-Z][a-zA-Z0-9._-]{2,40})',
        # Any line containing github
        r'.*github.*?([a-zA-Z][a-zA-Z0-9._-]{3,30}).*',
        # Standalone usernames near github
        r'([a-zA-Z][a-zA-Z0-9._-]{3,30}).*github',
        r'github.*?([a-zA-Z][a-zA-Z0-9._-]{3,30})',
        # Simple patterns
        r'(?:^|\s)([a-zA-Z][a-zA-Z0-9._-]{3,30})(?=.*github)',
        r'(?:github)(?:[^a-zA-Z0-9]*?)([a-zA-Z][a-zA-Z0-9._-]{3,30})'
    ]
    
    # Try each pattern and take first valid match
    for pattern in github_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            username = match.strip().rstrip('/')
            # Minimal validation - just check it's reasonable
            if (username and 
                len(username) >= 3 and len(username) <= 40 and
                username[0].isalpha() and
                not username.lower() in ['github', 'linkedin', 'twitter', 'facebook'] and
                not username.startswith(('http', 'www')) and
                not username.endswith(('.com', '.net', '.org'))):
                contact['github'] = f"https://github.com/{username}"
                break
        if 'github' in contact:
            break
    
    # Portfolio/Website patterns
    website_patterns = [
        r'(?:portfolio|website|personal site|site)[:\s]*(?:https?://)?([\w.-]+\.[a-z]{2,})/?',
        r'(?:https?://)([\w.-]+\.[a-z]{2,})(?=\s|$|\n)',
        r'(?:www\.)([\w.-]+\.[a-z]{2,})(?=\s|$|\n)',
        r'([\w-]+\.[a-z]{2,})(?=\s|$|\n)'
    ]
    
    for pattern in website_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            website = match.strip()
            if (not any(domain in website.lower() for domain in ['linkedin', 'github', 'gmail', 'yahoo', 'hotmail', 'outlook']) and
                '.' in website and len(website) > 4):
                if not website.startswith('http'):
                    website = f"https://{website}"
                contact['website'] = website
                break
        if 'website' in contact:
            break
    
    # Additional social media detection
    social_patterns = {
        'twitter': r'(?:twitter|@)[:\s]*([\w]+)',
        'instagram': r'(?:instagram)[:\s]*([\w.]+)',
        'behance': r'(?:behance)[:\s]*([\w.]+)'
    }
    
    for platform, pattern in social_patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            username = match.group(1)
            if len(username) > 2 and len(username) < 30:
                contact[platform] = f"https://{platform}.com/{username}"
    
    return contact

def extract_skills_ai(text: str, language: str) -> dict:
    """Multilingual AI skill extraction with language-specific patterns"""
    try:
        # Primary skill extraction using AI HR analyser
        skills = hr_analyser_instance._extract_skills_from_text(text)
        
        # Enhanced multilingual skill patterns for better accuracy
        multilingual_skill_patterns = {
            'programming': {
                'en': r'\b(?:python|java|javascript|react|angular|vue|node|php|ruby|go|rust|swift|kotlin|scala|c\+\+|c#|typescript|html|css|sql|mongodb|postgresql|mysql|redis|elasticsearch|docker|kubernetes|aws|azure|gcp|git|jenkins|terraform|ansible)\b',
                'de': r'\b(?:programmierung|entwicklung|softwareentwicklung|webentwicklung|datenbankentwicklung|frontend|backend|fullstack|programmiersprache|framework|bibliothek|api|datenbank|cloud|devops|versionskontrolle)\b',
                'es': r'\b(?:programación|desarrollo|desarrollo de software|desarrollo web|desarrollo de bases de datos|frontend|backend|fullstack|lenguaje de programación|framework|biblioteca|api|base de datos|nube|devops|control de versiones)\b',
                'fr': r'\b(?:programmation|développement|développement logiciel|développement web|développement de base de données|frontend|backend|fullstack|langage de programmation|framework|bibliothèque|api|base de données|cloud|devops|contrôle de version)\b',
                'it': r'\b(?:programmazione|sviluppo|sviluppo software|sviluppo web|sviluppo database|frontend|backend|fullstack|linguaggio di programmazione|framework|libreria|api|database|cloud|devops|controllo versione)\b',
                'pt': r'\b(?:programação|desenvolvimento|desenvolvimento de software|desenvolvimento web|desenvolvimento de banco de dados|frontend|backend|fullstack|linguagem de programação|framework|biblioteca|api|banco de dados|nuvem|devops|controle de versão)\b',
                'zh': r'(?:编程|开发|软件开发|网页开发|数据库开发|前端|后端|全栈|编程语言|框架|库|接口|数据库|云计算|运维|版本控制)',
                'ja': r'(?:プログラミング|開発|ソフトウェア開発|ウェブ開発|データベース開発|フロントエンド|バックエンド|フルスタック|プログラミング言語|フレームワーク|ライブラリ|API|データベース|クラウド|DevOps|バージョン管理)',
                'ru': r'\b(?:программирование|разработка|разработка программного обеспечения|веб-разработка|разработка баз данных|фронтенд|бэкенд|фуллстек|язык программирования|фреймворк|библиотека|api|база данных|облако|devops|контроль версий)\b',
                'ar': r'(?:برمجة|تطوير|تطوير البرمجيات|تطوير الويب|تطوير قواعد البيانات|الواجهة الأمامية|الواجهة الخلفية|مطور شامل|لغة برمجة|إطار عمل|مكتبة|واجهة برمجة|قاعدة بيانات|الحوسبة السحابية|عمليات التطوير|التحكم في الإصدار)'
            },
            'tools': {
                'en': r'\b(?:git|github|gitlab|bitbucket|jira|confluence|slack|teams|figma|sketch|photoshop|illustrator|indesign|office|excel|powerpoint|word|outlook|salesforce|hubspot|analytics|tableau|powerbi)\b',
                'de': r'\b(?:werkzeuge|tools|software|anwendungen|programme|systeme|plattformen|dienste|lösungen)\b',
                'es': r'\b(?:herramientas|software|aplicaciones|programas|sistemas|plataformas|servicios|soluciones)\b',
                'fr': r'\b(?:outils|logiciels|applications|programmes|systèmes|plateformes|services|solutions)\b',
                'it': r'\b(?:strumenti|software|applicazioni|programmi|sistemi|piattaforme|servizi|soluzioni)\b',
                'pt': r'\b(?:ferramentas|software|aplicações|programas|sistemas|plataformas|serviços|soluções)\b',
                'zh': r'(?:工具|软件|应用程序|程序|系统|平台|服务|解决方案)',
                'ja': r'(?:ツール|ソフトウェア|アプリケーション|プログラム|システム|プラットフォーム|サービス|ソリューション)',
                'ru': r'\b(?:инструменты|программное обеспечение|приложения|программы|системы|платформы|сервисы|решения)\b',
                'ar': r'(?:أدوات|برمجيات|تطبيقات|برامج|أنظمة|منصات|خدمات|حلول)'
            },
            'soft_skills': {
                'en': r'\b(?:leadership|management|communication|teamwork|collaboration|problem.solving|analytical|creative|innovative|adaptable|flexible|organized|detail.oriented|time.management|project.management|agile|scrum)\b',
                'de': r'\b(?:führung|management|kommunikation|teamarbeit|zusammenarbeit|problemlösung|analytisch|kreativ|innovativ|anpassungsfähig|flexibel|organisiert|detailorientiert|zeitmanagement|projektmanagement|agil|scrum)\b',
                'es': r'\b(?:liderazgo|gestión|comunicación|trabajo en equipo|colaboración|resolución de problemas|analítico|creativo|innovador|adaptable|flexible|organizado|orientado al detalle|gestión del tiempo|gestión de proyectos|ágil|scrum)\b',
                'fr': r'\b(?:leadership|gestion|communication|travail d\'équipe|collaboration|résolution de problèmes|analytique|créatif|innovant|adaptable|flexible|organisé|orienté détail|gestion du temps|gestion de projet|agile|scrum)\b',
                'it': r'\b(?:leadership|gestione|comunicazione|lavoro di squadra|collaborazione|risoluzione problemi|analitico|creativo|innovativo|adattabile|flessibile|organizzato|orientato ai dettagli|gestione del tempo|gestione progetti|agile|scrum)\b',
                'pt': r'\b(?:liderança|gestão|comunicação|trabalho em equipe|colaboração|resolução de problemas|analítico|criativo|inovador|adaptável|flexível|organizado|orientado a detalhes|gestão do tempo|gestão de projetos|ágil|scrum)\b',
                'zh': r'(?:领导力|管理|沟通|团队合作|协作|问题解决|分析|创意|创新|适应性|灵活|有组织|注重细节|时间管理|项目管理|敏捷|Scrum)',
                'ja': r'(?:リーダーシップ|マネジメント|コミュニケーション|チームワーク|コラボレーション|問題解決|分析的|創造的|革新的|適応性|柔軟性|組織的|細部重視|時間管理|プロジェクト管理|アジャイル|スクラム)',
                'ru': r'\b(?:лидерство|управление|коммуникация|командная работа|сотрудничество|решение проблем|аналитический|творческий|инновационный|адаптивный|гибкий|организованный|внимание к деталям|управление временем|управление проектами|agile|scrum)\b',
                'ar': r'(?:القيادة|الإدارة|التواصل|العمل الجماعي|التعاون|حل المشكلات|تحليلي|إبداعي|مبتكر|قابل للتكيف|مرن|منظم|موجه للتفاصيل|إدارة الوقت|إدارة المشاريع|رشيق|سكرم)'
            }
        }
        
        # Extract skills using language-specific patterns
        language_skills = set(skills)  # Start with AI-detected skills
        
        for category, patterns in multilingual_skill_patterns.items():
            # Use detected language pattern, fallback to English
            pattern = patterns.get(language, patterns.get('en', ''))
            if pattern:
                matches = re.findall(pattern, text, re.IGNORECASE)
                language_skills.update(matches)
        
        # Universal technical skill patterns (work across languages)
        universal_patterns = [
            r'\b(?:Python|Java|JavaScript|React|Angular|Vue|Node\.?js|PHP|Ruby|Go|Rust|Swift|Kotlin|Scala|C\+\+|C#|TypeScript|HTML5?|CSS3?|SQL|NoSQL|MongoDB|PostgreSQL|MySQL|Redis|Elasticsearch|Docker|Kubernetes|AWS|Azure|GCP|Git|Jenkins|Terraform|Ansible|Linux|Ubuntu|Windows|macOS|Apache|Nginx|REST|GraphQL|JSON|XML|API|SDK|IDE|VS Code|IntelliJ|Eclipse|Xcode|Android Studio)\b',
            r'\b(?:Machine Learning|Deep Learning|AI|Artificial Intelligence|Data Science|Big Data|Analytics|Statistics|Pandas|NumPy|TensorFlow|PyTorch|Scikit-learn|Jupyter|R|Matlab|Tableau|Power BI|Excel|Spark|Hadoop|Kafka|Airflow)\b',
            r'\b(?:Agile|Scrum|Kanban|DevOps|CI/CD|Microservices|Serverless|Cloud Computing|Blockchain|IoT|AR|VR|Mobile Development|Web Development|Frontend|Backend|Full Stack|UI/UX|Design Patterns|Testing|QA|Automation)\b'
        ]
        
        for pattern in universal_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            language_skills.update(matches)
        
        # Clean and categorize skills
        final_skills = list(set([skill.strip() for skill in language_skills if len(skill.strip()) > 1]))
        
        # Categorize skills intelligently
        categorized = {
            "Programming Languages": [s for s in final_skills if any(lang in s.lower() for lang in ['python', 'java', 'javascript', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala', 'c++', 'c#', 'typescript'])],
            "Web Technologies": [s for s in final_skills if any(web in s.lower() for web in ['react', 'angular', 'vue', 'html', 'css', 'node', 'express', 'django', 'flask', 'spring'])],
            "Databases": [s for s in final_skills if any(db in s.lower() for db in ['sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch', 'oracle', 'sqlite'])],
            "Cloud & DevOps": [s for s in final_skills if any(cloud in s.lower() for cloud in ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible', 'devops'])],
            "AI & Machine Learning": [s for s in final_skills if any(ai in s.lower() for ai in ['machine learning', 'deep learning', 'ai', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit'])],
            "Tools & Platforms": [s for s in final_skills if any(tool in s.lower() for tool in ['git', 'jira', 'confluence', 'figma', 'photoshop', 'office', 'tableau', 'powerbi'])],
            "All Skills": final_skills
        }
        
        return {"categorized": categorized, "all": final_skills}
        
    except Exception:
        return {"categorized": {"All Skills": []}, "all": []}

def extract_experience_ai(text: str, language: str) -> list:
    """Multilingual AI experience extraction with enhanced accuracy"""
    experiences = []
    
    # Comprehensive multilingual experience patterns
    exp_section_patterns = {
        'en': r'(?:experience|work\s+history|employment|professional\s+experience|career|work\s+experience|job\s+history|employment\s+history)\s*:?\s*\n(.*?)(?=\n\s*(?:education|skills|projects|certifications|awards|languages|references|$))',
        'de': r'(?:erfahrung|berufserfahrung|beschäftigung|arbeitserfahrung|beruflicher\s+werdegang|arbeitsplätze|anstellungen)\s*:?\s*\n(.*?)(?=\n\s*(?:bildung|ausbildung|fähigkeiten|projekte|zertifikate|auszeichnungen|sprachen|referenzen|$))',
        'es': r'(?:experiencia|historial\s+laboral|empleo|experiencia\s+profesional|carrera|experiencia\s+de\s+trabajo|historial\s+de\s+trabajo)\s*:?\s*\n(.*?)(?=\n\s*(?:educación|habilidades|proyectos|certificaciones|premios|idiomas|referencias|$))',
        'fr': r'(?:expérience|historique\s+de\s+travail|emploi|expérience\s+professionnelle|carrière|expérience\s+de\s+travail)\s*:?\s*\n(.*?)(?=\n\s*(?:éducation|formation|compétences|projets|certifications|prix|langues|références|$))',
        'it': r'(?:esperienza|storia\s+lavorativa|impiego|esperienza\s+professionale|carriera|esperienza\s+di\s+lavoro)\s*:?\s*\n(.*?)(?=\n\s*(?:istruzione|formazione|competenze|progetti|certificazioni|premi|lingue|riferimenti|$))',
        'pt': r'(?:experiência|histórico\s+de\s+trabalho|emprego|experiência\s+profissional|carreira|experiência\s+de\s+trabalho)\s*:?\s*\n(.*?)(?=\n\s*(?:educação|formação|habilidades|projetos|certificações|prêmios|idiomas|referências|$))',
        'zh': r'(?:经验|工作经历|就业|职业经验|职业生涯|工作经验|工作历史)\s*:?\s*\n(.*?)(?=\n\s*(?:教育|技能|项目|认证|奖项|语言|推荐|$))',
        'ja': r'(?:経験|職歴|雇用|職業経験|キャリア|仕事の経験|職歴)\s*:?\s*\n(.*?)(?=\n\s*(?:教育|学歴|スキル|プロジェクト|認定|賞|言語|参考|$))',
        'ru': r'(?:опыт|трудовая\s+деятельность|занятость|профессиональный\s+опыт|карьера|опыт\s+работы)\s*:?\s*\n(.*?)(?=\n\s*(?:образование|навыки|проекты|сертификаты|награды|языки|рекомендации|$))',
        'ar': r'(?:خبرة|تاريخ\s+العمل|التوظيف|الخبرة\s+المهنية|المسيرة\s+المهنية|خبرة\s+العمل)\s*:?\s*\n(.*?)(?=\n\s*(?:التعليم|المهارات|المشاريع|الشهادات|الجوائز|اللغات|المراجع|$))'
    }
    
    # Job title and company patterns
    job_patterns = {
        'en': r'(?:^|\n)\s*([A-Z][^\n]{10,80})\s*(?:\n|$)\s*(?:at\s+|@\s*)?([A-Z][^\n]{2,50})\s*(?:\n|$)\s*(\d{4}\s*[-–—]\s*(?:\d{4}|present|current))',
        'de': r'(?:^|\n)\s*([A-Z][^\n]{10,80})\s*(?:\n|$)\s*(?:bei\s+|@\s*)?([A-Z][^\n]{2,50})\s*(?:\n|$)\s*(\d{4}\s*[-–—]\s*(?:\d{4}|heute|aktuell))',
        'es': r'(?:^|\n)\s*([A-Z][^\n]{10,80})\s*(?:\n|$)\s*(?:en\s+|@\s*)?([A-Z][^\n]{2,50})\s*(?:\n|$)\s*(\d{4}\s*[-–—]\s*(?:\d{4}|presente|actual))',
        'fr': r'(?:^|\n)\s*([A-Z][^\n]{10,80})\s*(?:\n|$)\s*(?:chez\s+|à\s+|@\s*)?([A-Z][^\n]{2,50})\s*(?:\n|$)\s*(\d{4}\s*[-–—]\s*(?:\d{4}|présent|actuel))',
        'it': r'(?:^|\n)\s*([A-Z][^\n]{10,80})\s*(?:\n|$)\s*(?:presso\s+|@\s*)?([A-Z][^\n]{2,50})\s*(?:\n|$)\s*(\d{4}\s*[-–—]\s*(?:\d{4}|presente|attuale))',
        'pt': r'(?:^|\n)\s*([A-Z][^\n]{10,80})\s*(?:\n|$)\s*(?:na\s+|em\s+|@\s*)?([A-Z][^\n]{2,50})\s*(?:\n|$)\s*(\d{4}\s*[-–—]\s*(?:\d{4}|presente|atual))',
        'zh': r'(?:^|\n)\s*([^\n]{5,80})\s*(?:\n|$)\s*(?:在\s*)?([^\n]{2,50})\s*(?:\n|$)\s*(\d{4}\s*[-–—]\s*(?:\d{4}|现在|至今))',
        'ja': r'(?:^|\n)\s*([^\n]{5,80})\s*(?:\n|$)\s*(?:で\s*|にて\s*)?([^\n]{2,50})\s*(?:\n|$)\s*(\d{4}\s*[-–—]\s*(?:\d{4}|現在|至))',
        'ru': r'(?:^|\n)\s*([А-Я][^\n]{10,80})\s*(?:\n|$)\s*(?:в\s+|@\s*)?([А-Я][^\n]{2,50})\s*(?:\n|$)\s*(\d{4}\s*[-–—]\s*(?:\d{4}|настоящее время|сейчас))',
        'ar': r'(?:^|\n)\s*([^\n]{5,80})\s*(?:\n|$)\s*(?:في\s*)?([^\n]{2,50})\s*(?:\n|$)\s*(\d{4}\s*[-–—]\s*(?:\d{4}|الحاضر|الآن))'
    }
    
    # Extract experience section
    section_pattern = exp_section_patterns.get(language, exp_section_patterns['en'])
    section_match = re.search(section_pattern, text, re.IGNORECASE | re.DOTALL)
    
    if section_match:
        exp_text = section_match.group(1)
        
        # Extract individual jobs
        job_pattern = job_patterns.get(language, job_patterns['en'])
        job_matches = re.findall(job_pattern, exp_text, re.IGNORECASE | re.MULTILINE)
        
        for match in job_matches[:8]:  # Limit to 8 experiences
            title, company, duration = match
            
            # Extract skills from this experience
            job_context = f"{title} {company}"
            job_skills = hr_analyser_instance._extract_skills_from_text(job_context)
            
            experiences.append({
                "title": title.strip(),
                "company": company.strip(),
                "duration": duration.strip(),
                "description": f"Professional role at {company.strip()}",
                "skills_used": job_skills[:10]  # Top 10 skills
            })
    
    # Fallback: Universal patterns for any language
    if not experiences:
        universal_patterns = [
            r'(\d{4}\s*[-–—]\s*(?:\d{4}|present|heute|presente|présent|attuale|atual|现在|現在|настоящее время|الحاضر))\s*[:|\n]?\s*([^\n]{10,100})',
            r'([A-Z][^\n]{15,80})\s*\n\s*([A-Z][^\n]{5,50})\s*\n\s*(\d{4}\s*[-–—]\s*(?:\d{4}|present|current))'
        ]
        
        for pattern in universal_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches[:5]:
                if len(match) >= 2:
                    experiences.append({
                        "title": match[1] if len(match) > 1 else "Professional Role",
                        "company": "Company from resume",
                        "duration": match[0] if match[0] else "Not specified",
                        "description": "Experience extracted from resume",
                        "skills_used": hr_analyser_instance._extract_skills_from_text(' '.join(match))[:5]
                    })
    
    return experiences or [{
        "title": "Professional Experience", 
        "company": "Various Companies",
        "duration": "Multiple Years", 
        "description": "Professional experience found in resume",
        "skills_used": hr_analyser_instance._extract_skills_from_text(text)[:8]
    }]

def extract_projects_ai(text: str, language: str) -> list:
    """Multilingual AI project extraction with enhanced accuracy"""
    projects = []
    
    # Comprehensive multilingual project section patterns
    project_section_patterns = {
        'en': r'(?:projects?|portfolio|personal\s+projects?|side\s+projects?|academic\s+projects?|work\s+projects?)\s*:?\s*\n(.*?)(?=\n\s*(?:experience|education|skills|certifications|awards|languages|references|contact|$))',
        'de': r'(?:projekte?|portfolio|persönliche\s+projekte?|nebenprojekte?|akademische\s+projekte?|arbeitsprojekte?)\s*:?\s*\n(.*?)(?=\n\s*(?:erfahrung|bildung|fähigkeiten|zertifikate|auszeichnungen|sprachen|referenzen|kontakt|$))',
        'es': r'(?:proyectos?|portafolio|proyectos\s+personales?|proyectos\s+paralelos?|proyectos\s+académicos?|proyectos\s+de\s+trabajo?)\s*:?\s*\n(.*?)(?=\n\s*(?:experiencia|educación|habilidades|certificaciones|premios|idiomas|referencias|contacto|$))',
        'fr': r'(?:projets?|portfolio|projets\s+personnels?|projets\s+parallèles?|projets\s+académiques?|projets\s+de\s+travail?)\s*:?\s*\n(.*?)(?=\n\s*(?:expérience|éducation|compétences|certifications|prix|langues|références|contact|$))',
        'it': r'(?:progetti?|portfolio|progetti\s+personali?|progetti\s+paralleli?|progetti\s+accademici?|progetti\s+di\s+lavoro?)\s*:?\s*\n(.*?)(?=\n\s*(?:esperienza|istruzione|competenze|certificazioni|premi|lingue|riferimenti|contatto|$))',
        'pt': r'(?:projetos?|portfólio|projetos\s+pessoais?|projetos\s+paralelos?|projetos\s+acadêmicos?|projetos\s+de\s+trabalho?)\s*:?\s*\n(.*?)(?=\n\s*(?:experiência|educação|habilidades|certificações|prêmios|idiomas|referências|contato|$))',
        'zh': r'(?:项目|作品集|个人项目|业余项目|学术项目|工作项目)\s*:?\s*\n(.*?)(?=\n\s*(?:经验|教育|技能|认证|奖项|语言|推荐|联系|$))',
        'ja': r'(?:プロジェクト|ポートフォリオ|個人プロジェクト|サイドプロジェクト|学術プロジェクト|仕事のプロジェクト)\s*:?\s*\n(.*?)(?=\n\s*(?:経験|教育|スキル|認定|賞|言語|参考|連絡|$))',
        'ru': r'(?:проекты?|портфолио|личные\s+проекты?|побочные\s+проекты?|академические\s+проекты?|рабочие\s+проекты?)\s*:?\s*\n(.*?)(?=\n\s*(?:опыт|образование|навыки|сертификаты|награды|языки|рекомендации|контакт|$))',
        'ar': r'(?:مشاريع?|محفظة\s+أعمال|مشاريع\s+شخصية?|مشاريع\s+جانبية?|مشاريع\s+أكاديمية?|مشاريع\s+عمل?)\s*:?\s*\n(.*?)(?=\n\s*(?:خبرة|التعليم|المهارات|الشهادات|الجوائز|اللغات|المراجع|الاتصال|$))'
    }
    
    # Project title and description patterns
    project_item_patterns = {
        'en': r'(?:^|\n)\s*([A-Z][^\n]{5,100})\s*(?:\n|$)\s*([^\n]{20,300})(?:\n|$)\s*(?:Technologies?|Tech Stack|Built with|Using)\s*:?\s*([^\n]+)',
        'de': r'(?:^|\n)\s*([A-Z][^\n]{5,100})\s*(?:\n|$)\s*([^\n]{20,300})(?:\n|$)\s*(?:Technologien?|Tech Stack|Erstellt mit|Verwendet)\s*:?\s*([^\n]+)',
        'es': r'(?:^|\n)\s*([A-Z][^\n]{5,100})\s*(?:\n|$)\s*([^\n]{20,300})(?:\n|$)\s*(?:Tecnologías?|Stack Tecnológico|Construido con|Usando)\s*:?\s*([^\n]+)',
        'fr': r'(?:^|\n)\s*([A-Z][^\n]{5,100})\s*(?:\n|$)\s*([^\n]{20,300})(?:\n|$)\s*(?:Technologies?|Stack Technique|Construit avec|Utilisant)\s*:?\s*([^\n]+)',
        'it': r'(?:^|\n)\s*([A-Z][^\n]{5,100})\s*(?:\n|$)\s*([^\n]{20,300})(?:\n|$)\s*(?:Tecnologie?|Stack Tecnologico|Costruito con|Usando)\s*:?\s*([^\n]+)',
        'pt': r'(?:^|\n)\s*([A-Z][^\n]{5,100})\s*(?:\n|$)\s*([^\n]{20,300})(?:\n|$)\s*(?:Tecnologias?|Stack Tecnológico|Construído com|Usando)\s*:?\s*([^\n]+)',
        'zh': r'(?:^|\n)\s*([^\n]{3,100})\s*(?:\n|$)\s*([^\n]{10,300})(?:\n|$)\s*(?:技术|技术栈|使用技术|开发工具)\s*:?\s*([^\n]+)',
        'ja': r'(?:^|\n)\s*([^\n]{3,100})\s*(?:\n|$)\s*([^\n]{10,300})(?:\n|$)\s*(?:技術|技術スタック|使用技術|開発ツール)\s*:?\s*([^\n]+)',
        'ru': r'(?:^|\n)\s*([А-Я][^\n]{5,100})\s*(?:\n|$)\s*([^\n]{20,300})(?:\n|$)\s*(?:Технологии?|Технический стек|Построено с|Используя)\s*:?\s*([^\n]+)',
        'ar': r'(?:^|\n)\s*([^\n]{3,100})\s*(?:\n|$)\s*([^\n]{10,300})(?:\n|$)\s*(?:التقنيات?|المكدس التقني|مبني باستخدام|باستخدام)\s*:?\s*([^\n]+)'
    }
    
    # Extract projects section
    section_pattern = project_section_patterns.get(language, project_section_patterns['en'])
    section_match = re.search(section_pattern, text, re.IGNORECASE | re.DOTALL)
    
    if section_match:
        project_text = section_match.group(1)
        
        # Extract individual projects
        item_pattern = project_item_patterns.get(language, project_item_patterns['en'])
        project_matches = re.findall(item_pattern, project_text, re.IGNORECASE | re.MULTILINE)
        
        for match in project_matches[:10]:  # Limit to 10 projects
            title, description, tech_list = match
            
            # Extract technologies from description and tech list
            combined_text = f"{title} {description} {tech_list}"
            technologies = hr_analyser_instance._extract_skills_from_text(combined_text)
            
            # Parse additional technologies from tech list
            tech_items = re.split(r'[,;|\n]', tech_list)
            for item in tech_items:
                item = item.strip()
                if len(item) > 1 and len(item) < 30:
                    technologies.append(item)
            
            projects.append({
                "title": title.strip()[:150],
                "description": description.strip()[:500],
                "technologies": list(set(technologies))[:20],  # Remove duplicates, limit to 20
                "tech_stack": tech_list.strip()[:200]
            })
    
    # Fallback: Look for project-like content anywhere in resume
    if not projects:
        # Universal project patterns
        universal_patterns = [
            r'(?:^|\n)\s*([A-Z][^\n]{10,80})\s*(?:\n|$)\s*([^\n]{30,200})\s*(?:\n|$)\s*(?:GitHub|Demo|Live|Link|URL)\s*:?\s*([^\n]+)',
            r'(?:Built|Developed|Created|Designed|Implemented)\s+([^\n]{10,100})\s*(?:\n|$)\s*([^\n]{20,300})',
            r'([A-Z][^\n]{5,80})\s*[-–—]\s*([^\n]{20,200})\s*(?:\n|$)\s*(?:Technologies?|Tech|Stack|Tools?)\s*:?\s*([^\n]+)'
        ]
        
        for pattern in universal_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches[:8]:
                if len(match) >= 2:
                    title = match[0] if match[0] else "Project"
                    description = match[1] if len(match) > 1 else "Project description"
                    tech_info = match[2] if len(match) > 2 else ""
                    
                    combined_text = f"{title} {description} {tech_info}"
                    technologies = hr_analyser_instance._extract_skills_from_text(combined_text)
                    
                    projects.append({
                        "title": title.strip()[:150],
                        "description": description.strip()[:500],
                        "technologies": technologies[:15],
                        "tech_stack": tech_info.strip()[:200]
                    })
    
    return projects[:10] if projects else [{
        "title": "Technical Projects", 
        "description": "Project experience found throughout resume", 
        "technologies": hr_analyser_instance._extract_skills_from_text(text)[:10],
        "tech_stack": "Various technologies"
    }]

def extract_education_ai(text: str, language: str) -> list:
    """AI-enhanced education extraction"""
    education = []
    
    edu_patterns = [
        r'(?:bachelor|master|phd|degree|university|college|education|bachelor|master|promotion|abschluss|universität|hochschule|bildung|licenciatura|maestría|doctorado|grado|universidad|colegio|educación|licence|maîtrise|doctorat|diplôme|université|collège|éducation|laurea|master|dottorato|grado|università|collegio|istruzione|bacharelado|mestrado|doutorado|grau|universidade|faculdade|educação|学士|硕士|博士|学位|大学|学院|教育|学士|修士|博士|学位|大学|大学|教育)(.*?)(?:experience|skills|projects|$)',
        r'(?:b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?a\.?|ph\.?d\.?|bachelor|master|dr\.|prof\.).*?(?:in|of|en|de|di|em|在|で)\s*([^\n]+)',
        r'(\d{4})\s*(?:-|to|bis|a|à|a|至|まで)\s*(\d{4})\s*([^\n]+)'
    ]
    
    for pattern in edu_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches[:3]:
            if isinstance(match, tuple):
                edu_text = ' '.join(match)
            else:
                edu_text = match
            
            if len(edu_text.strip()) > 5:
                education.append({
                    "degree": edu_text.strip()[:100],
                    "institution": "Institution from resume",
                    "year": "Not specified"
                })
    
    return education

def analyse_strengths_ai(text: str, language: str) -> list:
    """Professional multilingual strength analysis"""
    skills_data = extract_skills_ai(text, language)
    strengths = []
    
    # Multilingual strength templates
    strength_templates = {
        "en": {
            "strong_expertise": "Strong expertise in {category} ({count} skills)",
            "good_foundation": "Good foundation in {category}",
            "diverse_skillset": "Diverse technical skill set with {count} technologies",
            "basic_foundation": "Solid technical foundation"
        },
        "de": {
            "strong_expertise": "Starke Expertise in {category} ({count} Fähigkeiten)",
            "good_foundation": "Gute Grundlage in {category}",
            "diverse_skillset": "Vielfältiges technisches Skill-Set mit {count} Technologien",
            "basic_foundation": "Solide technische Grundlage"
        },
        "es": {
            "strong_expertise": "Fuerte experiencia en {category} ({count} habilidades)",
            "good_foundation": "Buena base en {category}",
            "diverse_skillset": "Conjunto diverso de habilidades técnicas con {count} tecnologías",
            "basic_foundation": "Base técnica sólida"
        },
        "fr": {
            "strong_expertise": "Forte expertise en {category} ({count} compétences)",
            "good_foundation": "Bonne base en {category}",
            "diverse_skillset": "Ensemble diversifié de compétences techniques avec {count} technologies",
            "basic_foundation": "Base technique solide"
        }
    }
    
    templates = strength_templates.get(language, strength_templates["en"])
    
    for category, skills in skills_data["categorized"].items():
        if len(skills) >= 3:
            strengths.append(templates["strong_expertise"].format(category=category, count=len(skills)))
        elif len(skills) >= 1:
            strengths.append(templates["good_foundation"].format(category=category))
    
    if len(skills_data["all"]) >= 10:
        strengths.append(templates["diverse_skillset"].format(count=len(skills_data["all"])))
    
    return strengths or [templates["basic_foundation"]]

def analyse_weaknesses_ai(text: str, language: str) -> list:
    """Professional multilingual weakness analysis"""
    skills_data = extract_skills_ai(text, language)
    weaknesses = []
    
    # Multilingual weakness templates
    weakness_templates = {
        "en": {
            "limited_experience": "Limited experience in {category}",
            "expand_skillset": "Could expand technical skill set",
            "well_rounded": "Well-rounded skill profile"
        },
        "de": {
            "limited_experience": "Begrenzte Erfahrung in {category}",
            "expand_skillset": "Könnte technisches Skill-Set erweitern",
            "well_rounded": "Ausgewogenes Fähigkeitsprofil"
        },
        "es": {
            "limited_experience": "Experiencia limitada en {category}",
            "expand_skillset": "Podría ampliar el conjunto de habilidades técnicas",
            "well_rounded": "Perfil de habilidades bien equilibrado"
        },
        "fr": {
            "limited_experience": "Expérience limitée en {category}",
            "expand_skillset": "Pourrait élargir l'ensemble de compétences techniques",
            "well_rounded": "Profil de compétences bien équilibré"
        }
    }
    
    templates = weakness_templates.get(language, weakness_templates["en"])
    
    important_categories = ["Programming Languages", "Web Technologies", "Databases", "Cloud & DevOps"]
    missing_categories = [cat for cat in important_categories if cat not in skills_data["categorized"]]
    
    for category in missing_categories[:2]:
        weaknesses.append(templates["limited_experience"].format(category=category))
    
    if len(skills_data["all"]) < 5:
        weaknesses.append(templates["expand_skillset"])
    
    return weaknesses or [templates["well_rounded"]]

def generate_suggestions_ai(text: str, language: str) -> list:
    """AI-generated personalized improvement suggestions based on comprehensive resume analysis"""
    skills_data = extract_skills_ai(text, language)
    contact_data = extract_contact_ai(text)
    projects_data = extract_projects_ai(text, language)
    experience_data = extract_experience_ai(text, language)
    
    suggestions = []
    
    # Multilingual suggestion templates with AI-powered personalization
    suggestion_templates = {
        "en": {
            "missing_contact": "Add {contact_type} to improve professional visibility",
            "enhance_projects": "Add {count} more projects to showcase diverse skills",
            "quantify_impact": "Include metrics (users, performance, revenue) in {section}",
            "learn_trending": "Learn {skill} - high demand in current job market",
            "add_certifications": "Get certified in {skill} to validate expertise",
            "improve_descriptions": "Enhance {section} descriptions with specific achievements",
            "add_keywords": "Include industry keywords: {keywords}",
            "portfolio_website": "Create a portfolio website to showcase your work",
            "open_source": "Contribute to open source projects in {technology}",
            "networking": "Build professional network through {platform}",
            "skill_gap": "Bridge skill gap in {area} for better job matching",
            "leadership": "Highlight leadership experience and team management",
            "continuous_learning": "Show continuous learning through courses/workshops"
        },
        "de": {
            "missing_contact": "Fügen Sie {contact_type} hinzu, um die berufliche Sichtbarkeit zu verbessern",
            "enhance_projects": "Fügen Sie {count} weitere Projekte hinzu, um vielfältige Fähigkeiten zu zeigen",
            "quantify_impact": "Fügen Sie Metriken (Nutzer, Leistung, Umsatz) in {section} hinzu",
            "learn_trending": "Lernen Sie {skill} - hohe Nachfrage im aktuellen Arbeitsmarkt",
            "add_certifications": "Lassen Sie sich in {skill} zertifizieren, um Expertise zu validieren",
            "improve_descriptions": "Verbessern Sie {section}-Beschreibungen mit spezifischen Erfolgen",
            "add_keywords": "Fügen Sie Branchenschlüsselwörter hinzu: {keywords}",
            "portfolio_website": "Erstellen Sie eine Portfolio-Website, um Ihre Arbeit zu präsentieren",
            "open_source": "Tragen Sie zu Open-Source-Projekten in {technology} bei",
            "networking": "Bauen Sie ein professionelles Netzwerk über {platform} auf",
            "skill_gap": "Schließen Sie die Qualifikationslücke in {area} für bessere Job-Matching",
            "leadership": "Heben Sie Führungserfahrung und Teammanagement hervor",
            "continuous_learning": "Zeigen Sie kontinuierliches Lernen durch Kurse/Workshops"
        },
        "es": {
            "missing_contact": "Agregue {contact_type} para mejorar la visibilidad profesional",
            "enhance_projects": "Agregue {count} proyectos más para mostrar habilidades diversas",
            "quantify_impact": "Incluya métricas (usuarios, rendimiento, ingresos) en {section}",
            "learn_trending": "Aprenda {skill} - alta demanda en el mercado laboral actual",
            "add_certifications": "Certifíquese en {skill} para validar experiencia",
            "improve_descriptions": "Mejore las descripciones de {section} con logros específicos",
            "add_keywords": "Incluya palabras clave de la industria: {keywords}",
            "portfolio_website": "Cree un sitio web de portafolio para mostrar su trabajo",
            "open_source": "Contribuya a proyectos de código abierto en {technology}",
            "networking": "Construya una red profesional a través de {platform}",
            "skill_gap": "Cierre la brecha de habilidades en {area} para mejor coincidencia laboral",
            "leadership": "Destaque la experiencia de liderazgo y gestión de equipos",
            "continuous_learning": "Muestre aprendizaje continuo a través de cursos/talleres"
        },
        "fr": {
            "missing_contact": "Ajoutez {contact_type} pour améliorer la visibilité professionnelle",
            "enhance_projects": "Ajoutez {count} projets supplémentaires pour montrer des compétences diverses",
            "quantify_impact": "Incluez des métriques (utilisateurs, performance, revenus) dans {section}",
            "learn_trending": "Apprenez {skill} - forte demande sur le marché du travail actuel",
            "add_certifications": "Obtenez une certification en {skill} pour valider l'expertise",
            "improve_descriptions": "Améliorez les descriptions de {section} avec des réalisations spécifiques",
            "add_keywords": "Incluez des mots-clés de l'industrie: {keywords}",
            "portfolio_website": "Créez un site web de portfolio pour présenter votre travail",
            "open_source": "Contribuez aux projets open source en {technology}",
            "networking": "Construisez un réseau professionnel via {platform}",
            "skill_gap": "Comblez l'écart de compétences en {area} pour un meilleur matching d'emploi",
            "leadership": "Mettez en avant l'expérience de leadership et la gestion d'équipe",
            "continuous_learning": "Montrez l'apprentissage continu par des cours/ateliers"
        }
    }
    
    templates = suggestion_templates.get(language, suggestion_templates["en"])
    
    # AI-powered personalized suggestions based on resume analysis
    
    # 1. Contact Information Analysis
    missing_contacts = []
    if not contact_data.get('linkedin'):
        missing_contacts.append('LinkedIn profile')
    if not contact_data.get('github'):
        missing_contacts.append('GitHub profile')
    if not contact_data.get('website'):
        missing_contacts.append('portfolio website')
    
    if missing_contacts:
        suggestions.append(templates["missing_contact"].format(contact_type=missing_contacts[0]))
    
    # 2. Project Portfolio Analysis
    if len(projects_data) < 3:
        needed_projects = 3 - len(projects_data)
        suggestions.append(templates["enhance_projects"].format(count=needed_projects))
    
    # 3. Skills Gap Analysis with trending technologies
    trending_skills = ['Python', 'React', 'AWS', 'Docker', 'Kubernetes', 'Machine Learning', 'TypeScript', 'Node.js']
    missing_trending = [skill for skill in trending_skills if skill.lower() not in ' '.join(skills_data['all']).lower()]
    
    if missing_trending:
        suggestions.append(templates["learn_trending"].format(skill=missing_trending[0]))
    
    # 4. Quantifiable Achievements Analysis
    has_metrics = any(re.search(r'\d+%|\d+x|\d+ users|\d+ million|\d+ thousand|\$\d+', 
                               proj['description'] + ' ' + proj['title']) for proj in projects_data)
    
    if not has_metrics:
        suggestions.append(templates["quantify_impact"].format(section="projects and experience"))
    
    # 5. Certification Recommendations
    skill_categories = {
        'cloud': ['AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes'],
        'frontend': ['React', 'Angular', 'Vue.js', 'JavaScript', 'TypeScript'],
        'backend': ['Python', 'Java', 'Node.js', 'C#', 'Go'],
        'data': ['Python', 'SQL', 'Machine Learning', 'Data Science', 'Analytics']
    }
    
    user_skills_lower = [skill.lower() for skill in skills_data['all']]
    for category, category_skills in skill_categories.items():
        if any(skill.lower() in user_skills_lower for skill in category_skills):
            main_skill = next((skill for skill in category_skills if skill.lower() in user_skills_lower), category_skills[0])
            suggestions.append(templates["add_certifications"].format(skill=main_skill))
            break
    
    # 6. Professional Networking
    if not contact_data.get('linkedin'):
        suggestions.append(templates["networking"].format(platform="LinkedIn"))
    
    # 7. Portfolio Website Recommendation
    if not contact_data.get('website') and (len(projects_data) >= 2 or any('web' in proj['title'].lower() or 'app' in proj['title'].lower() for proj in projects_data)):
        suggestions.append(templates["portfolio_website"])
    
    # 8. Open Source Contribution
    if skills_data['all']:
        primary_tech = skills_data['all'][0] if skills_data['all'] else 'your technology stack'
        suggestions.append(templates["open_source"].format(technology=primary_tech))
    
    # 9. Industry Keywords
    common_keywords = ['Agile', 'Scrum', 'CI/CD', 'DevOps', 'API', 'Microservices', 'Cloud', 'Security']
    missing_keywords = [kw for kw in common_keywords if kw.lower() not in text.lower()]
    
    if missing_keywords:
        suggestions.append(templates["add_keywords"].format(keywords=', '.join(missing_keywords[:3])))
    
    # 10. Leadership and Soft Skills
    leadership_keywords = ['lead', 'manage', 'team', 'mentor', 'coordinate', 'supervise']
    has_leadership = any(keyword in text.lower() for keyword in leadership_keywords)
    
    if not has_leadership:
        suggestions.append(templates["leadership"])
    
    # 11. Continuous Learning
    learning_keywords = ['course', 'certification', 'workshop', 'training', 'bootcamp', 'udemy', 'coursera']
    shows_learning = any(keyword in text.lower() for keyword in learning_keywords)
    
    if not shows_learning:
        suggestions.append(templates["continuous_learning"])
    
    # 12. Skill Gap Analysis for Job Matching
    if len(skills_data['all']) < 8:
        suggestions.append(templates["skill_gap"].format(area="technical skills"))
    
    # Return top 8 most relevant suggestions
    return suggestions[:8]

@app.get("/")
async def root():
    return {"message": "AI-Powered Resume Analyser API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "resume-analyzer-api"}

@app.post("/api/analyse-resume")
async def analyse_resume(file: UploadFile = File(...), translate_to: Optional[str] = None):
    # Input validation
    if not file.filename or not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files supported")
    
    # File size validation (10MB limit)
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size too large. Maximum 10MB allowed")
    
    # Validate translate_to parameter
    if translate_to and translate_to not in ['en', 'de', 'es', 'fr', 'it', 'pt', 'zh', 'ja']:
        raise HTTPException(status_code=400, detail="Invalid translation language")
    
    try:
        content = await file.read()
        text = extract_text(content, file.filename)
        
        # Validate extracted text
        if not text or "Error extracting text" in text or len(text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Could not extract readable text from file")
        
        # Sanitize text length (prevent memory issues)
        if len(text) > 100000:  # 100KB limit
            text = text[:100000]
        
        # Detect language
        try:
            language = detect(text) if len(text.strip()) > 20 else "en"
        except:
            language = "en"
        
        # AI HR-powered comprehensive analysis
        try:
            comprehensive_skills = hr_analyser_instance.extract_all_skills_comprehensive(text)
            job_matches = hr_analyser_instance.analyse_job_fit_like_hr(text, comprehensive_skills)
        except (AttributeError, KeyError, TypeError, ValueError):
            # If AI HR analyser fails, create basic fallback
            try:
                # Try direct skill extraction from text
                fallback_skills = hr_analyser_instance._extract_skills_from_text(text)
                comprehensive_skills = {"all_skills": fallback_skills, "skills_section": [], "project_skills": [], "total_count": len(fallback_skills)}
                # Create basic job matches
                job_matches = [{"job_title": "Software Developer", "match_percentage": 50, "matching_skills": fallback_skills[:5], "missing_skills": ["Python", "JavaScript", "SQL"]}]
            except (AttributeError, KeyError, TypeError):
                comprehensive_skills = {"all_skills": [], "skills_section": [], "project_skills": [], "total_count": 0}
                job_matches = []
        
        # ATS Analysis with AI precision
        try:
            ats_analysis = ats_analyser_instance.analyse_ats_compatibility(text)
            ats_issues = ats_analyser_instance.scan_for_ats_issues(text)
        except Exception:
            # Fallback ATS analysis
            ats_analysis = {
                'ats_score': 75,
                'keyword_matches': {'matches': {}, 'scores': {}, 'total_score': 0},
                'format_score': 80,
                'readability_score': 75,
                'job_match_score': 0,
                'recommendations': ['Improve keyword optimization'],
                'missing_keywords': [],
                'ats_friendly': True
            }
            ats_issues = {'issues_found': 0, 'issues': [], 'ats_friendly': True}
        
        # Use AI HR analyser for all skill detection
        analysis = ai_analyse_resume(text, language)
        
        # Extract skills from all sections for comprehensive analysis
        all_extracted_skills = set()
        
        # Get skills from AI HR analyser
        if comprehensive_skills["all_skills"]:
            all_extracted_skills.update(comprehensive_skills["all_skills"])
        
        # Extract skills from projects section
        project_text = "\n".join([p["title"] + " " + p["description"] for p in analysis["projects"]])
        project_skills = hr_analyser_instance._extract_skills_from_text(project_text)
        all_extracted_skills.update(project_skills)
        
        # Extract skills from experience section
        experience_text = "\n".join([e["title"] + " " + e["description"] for e in analysis["experience"]])
        experience_skills = hr_analyser_instance._extract_skills_from_text(experience_text)
        all_extracted_skills.update(experience_skills)
        
        # Extract skills from achievements/awards section
        achievement_patterns = [
            r'(?:achievements?|awards?|accomplishments?|honors?|erfolge|auszeichnungen|leistungen|ehren|logros|premios|logros|honores|réalisations|prix|accomplissements|honneurs|risultati|premi|realizzazioni|onori|conquistas|prêmios|realizações|honras|成就|奖项|成绩|荣誉|実績|賞|成果|栄誉)(.*?)(?:experience|education|skills|projects|$)',
            r'(?:certified|certification|certificate|zertifiziert|zertifizierung|zertifikat|certificado|certificación|certificado|certifié|certification|certificat|certificato|certificazione|certificato|certificado|certificação|certificado|认证|证书|证明|認定|認証|証明書)[:\s]*([^\n]+)',
            r'(?:award|recognition|achievement|auszeichnung|anerkennung|erfolg|premio|reconocimiento|logro|prix|reconnaissance|réalisation|premio|riconoscimento|risultato|prêmio|reconhecimento|conquista|奖项|认可|成就|賞|認識|実績)[:\s]*([^\n]+)'
        ]
        
        achievement_text = ""
        for pattern in achievement_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                achievement_text += str(match) + " "
        
        if achievement_text:
            achievement_skills = hr_analyser_instance._extract_skills_from_text(achievement_text)
            all_extracted_skills.update(achievement_skills)
        
        # Update analysis with comprehensive skills
        final_skills = list(all_extracted_skills)
        analysis["skills"] = {
            "all": final_skills,
            "categorized": {
                "All Skills": final_skills,
                "From Projects": project_skills,
                "From Experience": experience_skills,
                "From Achievements": achievement_skills if achievement_text else []
            }
        }
        
        # Calculate overall compatibility score
        compatibility_score = job_matches[0]["match_percentage"] if job_matches else 50
        
        # Simple skill recommendations
        skill_recommendations = []
        for job in job_matches[:3]:
            missing_skills = job.get("missing_skills", [])
            if missing_skills:
                skill_recommendations.append({
                    "job_title": job["job_title"],
                    "priority_skills": missing_skills[:3],
                    "current_match": job["match_percentage"],
                    "projected_improvement": min(job["match_percentage"] + 15, 95)
                })
        
        # Professional multilingual translation
        def translate_response_to_language(response_data, target_language):
            if target_language == "en":
                return response_data
            
            try:
                # Translate job titles
                for job in response_data.get("job_matches", []):
                    job["job_title"] = translate_text(job["job_title"], target_language)
                
                # Translate strengths and weaknesses
                if "analysis" in response_data:
                    response_data["analysis"]["strengths"] = [translate_text(s, target_language) for s in response_data["analysis"]["strengths"]]
                    response_data["analysis"]["weaknesses"] = [translate_text(w, target_language) for w in response_data["analysis"]["weaknesses"]]
                
                # Translate suggestions
                response_data["suggestions"] = [translate_text(s, target_language) for s in response_data["suggestions"]]
                
                # Translate skill recommendations
                for rec in response_data.get("skill_recommendations", []):
                    rec["job_title"] = translate_text(rec["job_title"], target_language)
                
            except (KeyError, AttributeError, TypeError):
                pass  # Keep original if translation fails
            
            return response_data
        
        # Create professional response with prominent project and contact display
        response = {
            "extracted_data": {
                "name": analysis["name"],
                "language": language,
                "skills": analysis["skills"]["all"],
                "projects": analysis["projects"],
                "experience": analysis["experience"],
                "education": analysis["education"],
                "contact_info": {
                    "email": analysis["contact"].get("email", ""),
                    "phone": analysis["contact"].get("phone", ""),
                    "linkedin": analysis["contact"].get("linkedin", ""),
                    "github": analysis["contact"].get("github", ""),
                    "website": analysis["contact"].get("website", ""),
                    "twitter": analysis["contact"].get("twitter", ""),
                    "instagram": analysis["contact"].get("instagram", ""),
                    "behance": analysis["contact"].get("behance", "")
                }
            },
            "projects_summary": {
                "total_projects": len(analysis["projects"]),
                "project_list": [{
                    "title": p["title"],
                    "description": p["description"][:100] + "..." if len(p["description"]) > 100 else p["description"],
                    "technologies_used": p["technologies"]
                } for p in analysis["projects"]]
            },
            "professional_links": {
                "linkedin_profile": analysis["contact"].get("linkedin", ""),
                "github_profile": analysis["contact"].get("github", ""),
                "portfolio_website": analysis["contact"].get("website", ""),
                "has_linkedin": bool(analysis["contact"].get("linkedin")),
                "has_github": bool(analysis["contact"].get("github")),
                "has_portfolio": bool(analysis["contact"].get("website"))
            },
            "analysis": {
                "strengths": analysis["strengths"],
                "weaknesses": analysis["weaknesses"],
                "skill_analysis": {
                    "total_skills": len(analysis["skills"]["all"]),
                    "diversity_score": min(len(analysis["skills"]["all"]) * 3, 100),
                    "categorized_skills": analysis["skills"]["categorized"],
                    "skills_breakdown": {
                        "from_projects": len(analysis["skills"]["categorized"].get("From Projects", [])),
                        "from_experience": len(analysis["skills"]["categorized"].get("From Experience", [])),
                        "from_achievements": len(analysis["skills"]["categorized"].get("From Achievements", []))
                    }
                }
            },
            "job_matches": job_matches,
            "detected_categories": [{
                "category": "Technology",
                "confidence": float(compatibility_score),
                "match_strength": "Strong" if compatibility_score > 70 else "Moderate" if compatibility_score > 40 else "Weak"
            }],
            "compatibility_score": compatibility_score,
            "suggestions": analysis["suggestions"],
            "improvement_recommendations": {
                "priority_level": "high" if len(analysis["suggestions"]) > 6 else "medium" if len(analysis["suggestions"]) > 3 else "low",
                "total_suggestions": len(analysis["suggestions"]),
                "categories": {
                    "technical_skills": [s for s in analysis["suggestions"] if any(word in s.lower() for word in ['skill', 'learn', 'technology', 'certification'])],
                    "professional_presence": [s for s in analysis["suggestions"] if any(word in s.lower() for word in ['linkedin', 'github', 'portfolio', 'website', 'network'])],
                    "content_enhancement": [s for s in analysis["suggestions"] if any(word in s.lower() for word in ['project', 'metric', 'achievement', 'description', 'keyword'])],
                    "career_development": [s for s in analysis["suggestions"] if any(word in s.lower() for word in ['leadership', 'learning', 'open source', 'contribution'])]
                },
                "implementation_timeline": {
                    "immediate": [s for s in analysis["suggestions"][:3]],
                    "short_term": [s for s in analysis["suggestions"][3:6]],
                    "long_term": [s for s in analysis["suggestions"][6:]]
                }
            },
            "skill_recommendations": skill_recommendations,
            "detailed_projects": analysis["projects"],
            "contact_links": {
                "linkedin": analysis["contact"].get("linkedin", ""),
                "github": analysis["contact"].get("github", ""),
                "website": analysis["contact"].get("website", ""),
                "email": analysis["contact"].get("email", "")
            },
            "ats_analysis": {
                "ats_score": ats_analysis['ats_score'],
                "ats_friendly": ats_analysis['ats_friendly'],
                "keyword_optimization": {
                    "technical_keywords": len(ats_analysis['keyword_matches']['matches'].get('technical', [])),
                    "soft_skill_keywords": len(ats_analysis['keyword_matches']['matches'].get('soft_skills', [])),
                    "experience_keywords": len(ats_analysis['keyword_matches']['matches'].get('experience', [])),
                    "total_keyword_score": ats_analysis['keyword_matches']['total_score']
                },
                "format_analysis": {
                    "format_score": ats_analysis['format_score'],
                    "readability_score": ats_analysis['readability_score'],
                    "parsing_issues": ats_issues['issues_found'],
                    "issues_list": ats_issues['issues']
                },
                "ats_recommendations": ats_analysis['recommendations'],
                "missing_keywords": ats_analysis['missing_keywords'][:8],
                "compatibility_rating": "Excellent" if ats_analysis['ats_score'] >= 85 else "Good" if ats_analysis['ats_score'] >= 70 else "Needs Improvement" if ats_analysis['ats_score'] >= 50 else "Poor"
            }
        }
        
        # Translate response to detected language for native experience
        response = translate_response_to_language(response, language)
        
        # Add English translation option for international use
        if translate_to == "en" and language != "en":
            english_response = {
                "extracted_data": {
                    "name": analysis["name"],
                    "language": language,
                    "skills": analysis["skills"]["all"],
                    "projects": analysis["projects"],
                    "experience": analysis["experience"],
                    "education": analysis["education"],
                    "contact_info": {
                        "email": analysis["contact"].get("email", ""),
                        "phone": analysis["contact"].get("phone", ""),
                        "linkedin": analysis["contact"].get("linkedin", ""),
                        "github": analysis["contact"].get("github", ""),
                        "website": analysis["contact"].get("website", ""),
                        "twitter": analysis["contact"].get("twitter", ""),
                        "instagram": analysis["contact"].get("instagram", ""),
                        "behance": analysis["contact"].get("behance", "")
                    }
                },
                "projects_summary": {
                    "total_projects": len(analysis["projects"]),
                    "project_list": [{
                        "title": p["title"],
                        "description": p["description"][:100] + "..." if len(p["description"]) > 100 else p["description"],
                        "technologies_used": p["technologies"]
                    } for p in analysis["projects"]]
                },
                "professional_links": {
                    "linkedin_profile": analysis["contact"].get("linkedin", ""),
                    "github_profile": analysis["contact"].get("github", ""),
                    "portfolio_website": analysis["contact"].get("website", ""),
                    "has_linkedin": bool(analysis["contact"].get("linkedin")),
                    "has_github": bool(analysis["contact"].get("github")),
                    "has_portfolio": bool(analysis["contact"].get("website"))
                },
                "analysis": {
                    "strengths": [translate_to_english(s, language) for s in analysis["strengths"]],
                    "weaknesses": [translate_to_english(w, language) for w in analysis["weaknesses"]],
                    "skill_analysis": {
                        "total_skills": len(analysis["skills"]["all"]),
                        "diversity_score": min(len(analysis["skills"]["all"]) * 3, 100),
                        "categorized_skills": analysis["skills"]["categorized"]
                    }
                },
                "job_matches": [{**job, "job_title": translate_to_english(job["job_title"], language)} for job in job_matches],
                "detected_categories": response["detected_categories"],
                "compatibility_score": compatibility_score,
                "suggestions": [translate_to_english(s, language) for s in analysis["suggestions"]],
                "skill_recommendations": [{**rec, "job_title": translate_to_english(rec["job_title"], language)} for rec in skill_recommendations],
                "detailed_projects": analysis["projects"],
                "contact_links": {
                    "linkedin": analysis["contact"].get("linkedin", ""),
                    "github": analysis["contact"].get("github", ""),
                    "website": analysis["contact"].get("website", ""),
                    "email": analysis["contact"].get("email", "")
                },
                "ats_analysis": {
                    "ats_score": ats_analysis['ats_score'],
                    "ats_friendly": ats_analysis['ats_friendly'],
                    "keyword_optimization": {
                        "technical_keywords": len(ats_analysis['keyword_matches']['matches'].get('technical', [])),
                        "soft_skill_keywords": len(ats_analysis['keyword_matches']['matches'].get('soft_skills', [])),
                        "experience_keywords": len(ats_analysis['keyword_matches']['matches'].get('experience', [])),
                        "total_keyword_score": ats_analysis['keyword_matches']['total_score']
                    },
                    "format_analysis": {
                        "format_score": ats_analysis['format_score'],
                        "readability_score": ats_analysis['readability_score'],
                        "parsing_issues": ats_issues['issues_found'],
                        "issues_list": ats_issues['issues']
                    },
                    "ats_recommendations": ats_analysis['recommendations'],
                    "missing_keywords": ats_analysis['missing_keywords'][:8],
                    "compatibility_rating": "Excellent" if ats_analysis['ats_score'] >= 85 else "Good" if ats_analysis['ats_score'] >= 70 else "Needs Improvement" if ats_analysis['ats_score'] >= 50 else "Poor"
                },
                "translated_to": "en",
                "original_language": language
            }
            return english_response
        
        return response
    
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error processing file: Unable to analyse resume")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)