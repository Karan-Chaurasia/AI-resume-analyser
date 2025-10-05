import re
from typing import Dict, List, Any

class AIHRAnalyser:
    def __init__(self):
        self.job_profiles = {
            # Software Engineering
            "Senior Software Engineer": {
                "core_skills": ["Python", "Java", "JavaScript", "C++", "C#", "Go", "Rust"],
                "framework_skills": ["React", "Angular", "Vue.js", "Django", "Flask", "Spring", "Express"],
                "database_skills": ["SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis"],
                "tools_skills": ["Git", "Docker", "Kubernetes", "Jenkins", "AWS", "Azure"],
                "project_indicators": ["architecture", "scalable", "microservices", "api", "full-stack", "backend", "frontend"],
                "experience_weight": 0.4, "skills_weight": 0.35, "projects_weight": 0.25, "min_skills": 8, "seniority": "senior"
            },
            "Full Stack Developer": {
                "core_skills": ["JavaScript", "TypeScript", "Python", "Java", "C#"],
                "framework_skills": ["React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask"],
                "database_skills": ["SQL", "MongoDB", "PostgreSQL", "MySQL"],
                "tools_skills": ["Git", "REST API", "GraphQL", "HTML", "CSS", "Bootstrap"],
                "project_indicators": ["full-stack", "web application", "frontend", "backend", "responsive", "spa"],
                "experience_weight": 0.3, "skills_weight": 0.4, "projects_weight": 0.3, "min_skills": 6, "seniority": "mid"
            },
            "Frontend Developer": {
                "core_skills": ["JavaScript", "TypeScript", "HTML", "CSS"],
                "framework_skills": ["React", "Angular", "Vue.js", "Next.js", "Nuxt.js"],
                "database_skills": ["REST API", "GraphQL", "Firebase"],
                "tools_skills": ["Git", "Webpack", "Sass", "Bootstrap", "Tailwind", "Figma"],
                "project_indicators": ["frontend", "ui", "responsive", "spa", "pwa", "user interface", "web design"],
                "experience_weight": 0.25, "skills_weight": 0.45, "projects_weight": 0.3, "min_skills": 5, "seniority": "mid"
            },
            "Backend Developer": {
                "core_skills": ["Python", "Java", "Node.js", "C#", "Go", "PHP"],
                "framework_skills": ["Django", "Flask", "Spring", "Express", "FastAPI", "Laravel"],
                "database_skills": ["SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis"],
                "tools_skills": ["Git", "Docker", "REST API", "GraphQL", "Microservices"],
                "project_indicators": ["backend", "api", "server", "database", "microservices", "rest", "graphql"],
                "experience_weight": 0.35, "skills_weight": 0.4, "projects_weight": 0.25, "min_skills": 6, "seniority": "mid"
            },
            "Junior Software Developer": {
                "core_skills": ["Python", "Java", "JavaScript", "C++", "C#"],
                "framework_skills": ["React", "Django", "Flask", "Spring"],
                "database_skills": ["SQL", "MySQL", "PostgreSQL"],
                "tools_skills": ["Git", "HTML", "CSS"],
                "project_indicators": ["programming", "coding", "development", "software"],
                "experience_weight": 0.2, "skills_weight": 0.5, "projects_weight": 0.3, "min_skills": 3, "seniority": "junior"
            },
            
            # Data & AI
            "Data Scientist": {
                "core_skills": ["Python", "R", "SQL", "Statistics", "Machine Learning"],
                "framework_skills": ["Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Keras"],
                "database_skills": ["SQL", "PostgreSQL", "MongoDB", "BigQuery", "Snowflake"],
                "tools_skills": ["Jupyter", "Git", "Docker", "AWS", "Azure", "Tableau", "Power BI"],
                "project_indicators": ["machine learning", "data analysis", "predictive model", "classification", "regression", "deep learning", "nlp", "computer vision"],
                "experience_weight": 0.35, "skills_weight": 0.35, "projects_weight": 0.3, "min_skills": 7, "seniority": "mid"
            },
            "Machine Learning Engineer": {
                "core_skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"],
                "framework_skills": ["Scikit-learn", "Keras", "MLflow", "Kubeflow", "Apache Spark"],
                "database_skills": ["SQL", "MongoDB", "Redis", "BigQuery"],
                "tools_skills": ["Docker", "Kubernetes", "AWS", "Git", "Jupyter", "MLOps"],
                "project_indicators": ["ml model", "deep learning", "neural network", "ai", "model deployment", "mlops"],
                "experience_weight": 0.3, "skills_weight": 0.4, "projects_weight": 0.3, "min_skills": 6, "seniority": "mid"
            },
            "Data Engineer": {
                "core_skills": ["Python", "SQL", "Apache Spark", "Hadoop", "Kafka"],
                "framework_skills": ["Airflow", "Pandas", "NumPy", "Databricks"],
                "database_skills": ["PostgreSQL", "MongoDB", "Redis", "Snowflake", "BigQuery"],
                "tools_skills": ["Docker", "Kubernetes", "AWS", "Azure", "Git", "ETL"],
                "project_indicators": ["data pipeline", "etl", "data warehouse", "big data", "streaming"],
                "experience_weight": 0.35, "skills_weight": 0.35, "projects_weight": 0.3, "min_skills": 6, "seniority": "mid"
            },
            "Data Analyst": {
                "core_skills": ["SQL", "Python", "R", "Statistics", "Excel"],
                "framework_skills": ["Pandas", "NumPy", "Matplotlib", "Seaborn"],
                "database_skills": ["SQL", "PostgreSQL", "MySQL"],
                "tools_skills": ["Tableau", "Power BI", "Jupyter", "Git"],
                "project_indicators": ["data analysis", "reporting", "dashboard", "visualization", "insights"],
                "experience_weight": 0.3, "skills_weight": 0.4, "projects_weight": 0.3, "min_skills": 4, "seniority": "junior"
            },
            
            # DevOps & Infrastructure
            "DevOps Engineer": {
                "core_skills": ["Linux", "Python", "Bash", "Docker", "Kubernetes"],
                "framework_skills": ["Terraform", "Ansible", "Chef", "Puppet"],
                "database_skills": ["SQL", "PostgreSQL", "MongoDB", "Redis"],
                "tools_skills": ["AWS", "Azure", "GCP", "Jenkins", "GitLab CI", "Git", "Monitoring"],
                "project_indicators": ["infrastructure", "deployment", "ci/cd", "automation", "cloud", "containerization", "orchestration"],
                "experience_weight": 0.4, "skills_weight": 0.3, "projects_weight": 0.3, "min_skills": 6, "seniority": "mid"
            },
            "Cloud Architect": {
                "core_skills": ["AWS", "Azure", "GCP", "Cloud Architecture", "Microservices"],
                "framework_skills": ["Terraform", "CloudFormation", "Kubernetes", "Docker"],
                "database_skills": ["DynamoDB", "RDS", "CosmosDB", "BigQuery"],
                "tools_skills": ["Jenkins", "Git", "Monitoring", "Security", "Networking"],
                "project_indicators": ["cloud migration", "architecture", "scalability", "high availability", "disaster recovery"],
                "experience_weight": 0.45, "skills_weight": 0.3, "projects_weight": 0.25, "min_skills": 7, "seniority": "senior"
            },
            "Site Reliability Engineer": {
                "core_skills": ["Linux", "Python", "Go", "Monitoring", "Incident Response"],
                "framework_skills": ["Prometheus", "Grafana", "Kubernetes", "Docker"],
                "database_skills": ["SQL", "Redis", "InfluxDB"],
                "tools_skills": ["AWS", "Git", "Terraform", "Ansible", "Alerting"],
                "project_indicators": ["reliability", "monitoring", "sla", "incident", "automation", "performance"],
                "experience_weight": 0.4, "skills_weight": 0.3, "projects_weight": 0.3, "min_skills": 6, "seniority": "mid"
            },
            
            # Mobile Development
            "Mobile Developer": {
                "core_skills": ["Swift", "Kotlin", "Java", "Dart", "JavaScript"],
                "framework_skills": ["React Native", "Flutter", "Xamarin", "Ionic"],
                "database_skills": ["SQLite", "Firebase", "Realm", "Core Data"],
                "tools_skills": ["Xcode", "Android Studio", "Git", "REST API"],
                "project_indicators": ["mobile", "ios", "android", "app", "react native", "flutter"],
                "experience_weight": 0.3, "skills_weight": 0.4, "projects_weight": 0.3, "min_skills": 4, "seniority": "mid"
            },
            "iOS Developer": {
                "core_skills": ["Swift", "Objective-C", "iOS", "Xcode"],
                "framework_skills": ["SwiftUI", "UIKit", "Core Data", "Combine"],
                "database_skills": ["Core Data", "SQLite", "Firebase"],
                "tools_skills": ["Xcode", "Git", "TestFlight", "App Store Connect"],
                "project_indicators": ["ios", "iphone", "ipad", "app store", "swift"],
                "experience_weight": 0.3, "skills_weight": 0.4, "projects_weight": 0.3, "min_skills": 4, "seniority": "mid"
            },
            "Android Developer": {
                "core_skills": ["Kotlin", "Java", "Android", "Android Studio"],
                "framework_skills": ["Jetpack Compose", "Room", "Retrofit", "Dagger"],
                "database_skills": ["Room", "SQLite", "Firebase"],
                "tools_skills": ["Android Studio", "Git", "Google Play Console", "Gradle"],
                "project_indicators": ["android", "google play", "kotlin", "mobile app"],
                "experience_weight": 0.3, "skills_weight": 0.4, "projects_weight": 0.3, "min_skills": 4, "seniority": "mid"
            },
            
            # Design & UX
            "UI/UX Designer": {
                "core_skills": ["Figma", "Sketch", "Adobe XD", "User Research", "Prototyping"],
                "framework_skills": ["Design Systems", "Wireframing", "User Testing", "Information Architecture"],
                "database_skills": ["User Analytics", "A/B Testing"],
                "tools_skills": ["Photoshop", "Illustrator", "InVision", "Principle", "Zeplin"],
                "project_indicators": ["ui design", "ux design", "user experience", "interface", "usability", "design system"],
                "experience_weight": 0.3, "skills_weight": 0.4, "projects_weight": 0.3, "min_skills": 4, "seniority": "mid"
            },
            "Product Designer": {
                "core_skills": ["Figma", "User Research", "Product Strategy", "Design Thinking"],
                "framework_skills": ["Prototyping", "User Journey Mapping", "Design Systems"],
                "database_skills": ["Analytics", "User Data"],
                "tools_skills": ["Sketch", "Adobe Creative Suite", "Miro", "Notion"],
                "project_indicators": ["product design", "user journey", "product strategy", "design thinking"],
                "experience_weight": 0.35, "skills_weight": 0.35, "projects_weight": 0.3, "min_skills": 4, "seniority": "mid"
            },
            
            # Security
            "Cybersecurity Analyst": {
                "core_skills": ["Cybersecurity", "Network Security", "Incident Response", "Risk Assessment"],
                "framework_skills": ["SIEM", "Penetration Testing", "Vulnerability Assessment", "Forensics"],
                "database_skills": ["SQL", "Log Analysis"],
                "tools_skills": ["Wireshark", "Nmap", "Metasploit", "Burp Suite", "Splunk"],
                "project_indicators": ["security", "penetration test", "vulnerability", "incident response", "threat analysis"],
                "experience_weight": 0.4, "skills_weight": 0.35, "projects_weight": 0.25, "min_skills": 5, "seniority": "mid"
            },
            
            # Quality Assurance
            "QA Engineer": {
                "core_skills": ["Testing", "Test Automation", "Selenium", "Quality Assurance"],
                "framework_skills": ["Cypress", "Jest", "TestNG", "JUnit", "Playwright"],
                "database_skills": ["SQL", "Database Testing"],
                "tools_skills": ["JIRA", "Git", "Postman", "Jenkins", "TestRail"],
                "project_indicators": ["testing", "automation", "quality assurance", "test cases", "bug tracking"],
                "experience_weight": 0.3, "skills_weight": 0.4, "projects_weight": 0.3, "min_skills": 4, "seniority": "mid"
            },
            
            # Business & Product
            "Product Manager": {
                "core_skills": ["Product Strategy", "Roadmap Planning", "Stakeholder Management", "Market Research"],
                "framework_skills": ["Agile", "Scrum", "User Stories", "A/B Testing"],
                "database_skills": ["Analytics", "SQL", "Data Analysis"],
                "tools_skills": ["JIRA", "Confluence", "Figma", "Google Analytics", "Mixpanel"],
                "project_indicators": ["product management", "roadmap", "feature", "user story", "market research"],
                "experience_weight": 0.4, "skills_weight": 0.3, "projects_weight": 0.3, "min_skills": 5, "seniority": "mid"
            },
            "Business Analyst": {
                "core_skills": ["Business Analysis", "Requirements Gathering", "Process Improvement", "Stakeholder Management"],
                "framework_skills": ["Agile", "Waterfall", "BPMN", "Use Cases"],
                "database_skills": ["SQL", "Data Analysis", "Reporting"],
                "tools_skills": ["Excel", "Visio", "JIRA", "Confluence", "Power BI"],
                "project_indicators": ["business analysis", "requirements", "process improvement", "stakeholder"],
                "experience_weight": 0.4, "skills_weight": 0.3, "projects_weight": 0.3, "min_skills": 4, "seniority": "mid"
            },
            
            # Specialized Roles
            "Game Developer": {
                "core_skills": ["Unity", "C#", "Unreal Engine", "C++", "Game Design"],
                "framework_skills": ["3D Graphics", "Physics", "AI", "Networking"],
                "database_skills": ["Game Databases", "Player Data"],
                "tools_skills": ["Blender", "Maya", "Git", "Perforce", "Visual Studio"],
                "project_indicators": ["game development", "unity", "unreal", "3d", "gaming", "interactive"],
                "experience_weight": 0.3, "skills_weight": 0.4, "projects_weight": 0.3, "min_skills": 5, "seniority": "mid"
            },
            "Blockchain Developer": {
                "core_skills": ["Solidity", "Blockchain", "Smart Contracts", "Web3", "Ethereum"],
                "framework_skills": ["Truffle", "Hardhat", "React", "Node.js"],
                "database_skills": ["IPFS", "MongoDB", "Graph Databases"],
                "tools_skills": ["MetaMask", "Git", "Remix", "Ganache"],
                "project_indicators": ["blockchain", "smart contract", "defi", "nft", "cryptocurrency", "web3"],
                "experience_weight": 0.3, "skills_weight": 0.4, "projects_weight": 0.3, "min_skills": 5, "seniority": "mid"
            },
            "Technical Writer": {
                "core_skills": ["Technical Writing", "Documentation", "API Documentation", "Content Strategy"],
                "framework_skills": ["Markdown", "Git", "Content Management", "Information Architecture"],
                "database_skills": ["Content Databases", "CMS"],
                "tools_skills": ["Confluence", "Notion", "GitBook", "Swagger", "Postman"],
                "project_indicators": ["documentation", "technical writing", "api docs", "user guide", "content"],
                "experience_weight": 0.3, "skills_weight": 0.4, "projects_weight": 0.3, "min_skills": 3, "seniority": "junior"
            }
        }
    
    def extract_all_skills_comprehensive(self, text: str) -> Dict[str, List[str]]:
        """Extract skills comprehensively from entire resume text"""
        
        # Extract from entire text first for maximum coverage
        all_text_skills = self._extract_skills_from_text(text)
        
        # Find specific sections for detailed analysis
        skills_section = self._find_section(text, ["skills", "technical skills", "competencies", "technologies", "expertise", "proficiencies", "core competencies"])
        projects_section = self._find_section(text, ["projects", "project experience", "portfolio", "work samples", "personal projects"])
        experience_section = self._find_section(text, ["experience", "work experience", "professional experience", "employment", "career history"])
        
        # Extract from specific sections
        skills_from_section = self._extract_skills_from_text(skills_section) if skills_section else []
        skills_from_projects = self._extract_skills_from_text(projects_section) if projects_section else []
        skills_from_experience = self._extract_skills_from_text(experience_section) if experience_section else []
        
        # Combine all sources for maximum skill detection
        combined_skills = list(set(all_text_skills + skills_from_section + skills_from_projects + skills_from_experience))
        
        return {
            "skills_section": skills_from_section,
            "project_skills": skills_from_projects,
            "experience_skills": skills_from_experience,
            "all_skills": combined_skills,
            "total_count": len(combined_skills)
        }
    
    def _find_section(self, text: str, keywords: List[str]) -> str:
        """Find specific section in resume with improved detection"""
        lines = text.split('\n')
        start_idx = -1
        
        # Look for section headers
        for i, line in enumerate(lines):
            line_clean = line.strip().lower()
            if len(line_clean) == 0:
                continue
                
            for keyword in keywords:
                # Check if line contains keyword and looks like a header
                if (keyword.lower() in line_clean and 
                    (len(line_clean) < 80 or  # Short lines are likely headers
                     line_clean.endswith(':') or  # Lines ending with colon
                     line.isupper() or  # All caps headers
                     re.match(r'^[A-Z][^a-z]*$', line.strip()) or  # Title case headers
                     re.match(r'^\s*[-=*]{2,}', line))):
                    start_idx = i
                    break
            if start_idx != -1:
                break
        
        if start_idx == -1:
            return ""
        
        # Find next section or end of text
        end_idx = len(lines)
        section_keywords = ['experience', 'education', 'projects', 'skills', 'certifications', 'awards', 'achievements', 'qualifications', 'summary', 'objective', 'contact']
        
        for i in range(start_idx + 1, len(lines)):
            line = lines[i].strip().lower()
            if len(line) == 0:
                continue
                
            # Check if this looks like a new section header
            is_header = (len(line) < 80 or line.endswith(':') or 
                        lines[i].isupper() or 
                        re.match(r'^[A-Z][^a-z]*$', lines[i].strip()) or
                        re.match(r'^\s*[-=*]{2,}', lines[i]))
            
            if is_header:
                for section_kw in section_keywords:
                    if section_kw in line and not any(kw in line for kw in keywords):
                        end_idx = i
                        break
                if end_idx != len(lines):
                    break
        
        return '\n'.join(lines[start_idx:end_idx])
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract technical skills comprehensively from any language"""
        
        # Comprehensive multilingual skill database
        skills_database = [
            # Programming Languages
            "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "PHP", "Ruby", "Go", "Rust", "Swift", "Kotlin", "Scala", "R", "MATLAB", "Perl", "Dart", "Lua", "Objective-C", "C", "Assembly", "Fortran", "COBOL", "Haskell", "Clojure", "Erlang", "F#", "VB.NET", "Julia", "Groovy", "Elixir",
            
            # Web Frontend
            "React", "Angular", "Vue.js", "Vue", "Svelte", "Next.js", "Nuxt.js", "Gatsby", "Ember.js", "jQuery", "HTML", "HTML5", "CSS", "CSS3", "SASS", "SCSS", "LESS", "Bootstrap", "Tailwind CSS", "Tailwind", "Material-UI", "Ant Design", "Webpack", "Vite", "Babel", "ESLint", "Prettier",
            
            # Web Backend
            "Node.js", "Express", "Koa", "Fastify", "NestJS", "Django", "Flask", "FastAPI", "Spring", "Spring Boot", "Hibernate", "Laravel", "Symfony", "CodeIgniter", "Rails", "Ruby on Rails", "ASP.NET", "ASP.NET Core", ".NET", ".NET Core", "Gin", "Echo", "Fiber",
            
            # Databases
            "MySQL", "PostgreSQL", "SQLite", "Oracle", "SQL Server", "MariaDB", "MongoDB", "CouchDB", "Redis", "Memcached", "Cassandra", "HBase", "Neo4j", "InfluxDB", "DynamoDB", "Firebase", "Firestore", "SQL", "NoSQL", "GraphQL",
            
            # Cloud Platforms
            "AWS", "Amazon Web Services", "Azure", "Microsoft Azure", "Google Cloud", "GCP", "Google Cloud Platform", "IBM Cloud", "DigitalOcean", "Heroku", "Netlify", "Vercel",
            
            # DevOps & Infrastructure
            "Docker", "Kubernetes", "K8s", "Jenkins", "GitLab CI", "GitHub Actions", "CircleCI", "Travis CI", "Terraform", "CloudFormation", "Ansible", "Chef", "Puppet", "Vagrant", "NGINX", "Apache",
            
            # Version Control
            "Git", "GitHub", "GitLab", "Bitbucket", "SVN", "Mercurial",
            
            # AI/ML/Data Science
            "Machine Learning", "Deep Learning", "Neural Networks", "Artificial Intelligence", "Data Science", "Data Analysis", "Statistics", "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "XGBoost", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "OpenCV", "NLTK", "spaCy", "Computer Vision", "NLP", "Natural Language Processing", "Jupyter", "Apache Spark", "Hadoop", "Kafka", "Airflow",
            
            # Mobile Development
            "iOS", "Android", "React Native", "Flutter", "Xamarin", "Ionic", "Unity", "Xcode", "Android Studio", "SwiftUI", "UIKit",
            
            # Testing
            "Jest", "Mocha", "Chai", "Jasmine", "Cypress", "Selenium", "TestNG", "JUnit", "PyTest", "RSpec", "PHPUnit", "Postman", "JMeter",
            
            # Operating Systems
            "Linux", "Ubuntu", "CentOS", "RHEL", "Debian", "Unix", "macOS", "Windows", "Windows Server",
            
            # Shells & Scripting
            "Bash", "PowerShell", "Shell Scripting", "AWK", "Sed",
            
            # IDEs & Editors
            "VS Code", "Visual Studio", "IntelliJ IDEA", "PyCharm", "WebStorm", "Eclipse", "NetBeans", "Atom", "Sublime Text", "Vim", "Emacs",
            
            # Design & UI/UX
            "Figma", "Sketch", "Adobe XD", "Photoshop", "Illustrator", "UI/UX", "User Experience", "User Interface", "Wireframing", "Prototyping",
            
            # Project Management
            "Agile", "Scrum", "Kanban", "JIRA", "Trello", "Asana", "Slack", "Microsoft Teams",
            
            # Security
            "Cybersecurity", "Information Security", "OWASP", "Penetration Testing", "OAuth", "JWT", "SSL/TLS",
            
            # Other Technologies
            "REST API", "REST", "API", "Microservices", "SOA", "WebSocket", "Blockchain", "IoT", "AR", "VR", "PWA", "SPA", "Serverless", "Lambda", "Event-Driven Architecture", "Message Queues", "RabbitMQ", "WebRTC", "Apollo", "Prisma"
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        # Direct skill matching with fuzzy logic
        for skill in skills_database:
            skill_lower = skill.lower()
            
            # Exact match
            if re.search(r'\b' + re.escape(skill_lower) + r'\b', text_lower):
                found_skills.append(skill)
                continue
            
            # Common variations
            variations = {
                'javascript': ['js', 'ecmascript'],
                'typescript': ['ts'],
                'react': ['reactjs', 'react.js'],
                'vue': ['vuejs', 'vue.js'],
                'node.js': ['nodejs', 'node'],
                'postgresql': ['postgres'],
                'mongodb': ['mongo'],
                'kubernetes': ['k8s'],
                'machine learning': ['ml'],
                'artificial intelligence': ['ai'],
                'natural language processing': ['nlp'],
                'user interface': ['ui'],
                'user experience': ['ux'],
                'amazon web services': ['aws'],
                'google cloud platform': ['gcp'],
                'microsoft azure': ['azure']
            }
            
            if skill_lower in variations:
                for variation in variations[skill_lower]:
                    if re.search(r'\b' + re.escape(variation) + r'\b', text_lower):
                        found_skills.append(skill)
                        break
        
        # Clean and deduplicate
        cleaned_skills = []
        for skill in found_skills:
            skill = skill.strip()
            if len(skill) > 1 and skill not in cleaned_skills:
                cleaned_skills.append(skill)
        
        return cleaned_skills
    
    def analyse_job_fit_like_hr(self, text: str, extracted_skills: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Analyse job fit like an experienced HR professional"""
        
        all_skills = [skill.lower() for skill in extracted_skills["all_skills"]]
        skills_section_skills = [skill.lower() for skill in extracted_skills["skills_section"]]
        project_skills = [skill.lower() for skill in extracted_skills["project_skills"]]
        
        job_matches = []
        
        for job_title, profile in self.job_profiles.items():
            # Calculate skill matches across categories
            core_matches = self._count_skill_matches(all_skills, profile["core_skills"])
            framework_matches = self._count_skill_matches(all_skills, profile["framework_skills"])
            database_matches = self._count_skill_matches(all_skills, profile["database_skills"])
            tools_matches = self._count_skill_matches(all_skills, profile["tools_skills"])
            
            # Project relevance analysis
            project_relevance = self._analyse_project_relevance(text, profile["project_indicators"])
            
            # Calculate weighted scores
            skill_score = (core_matches * 3 + framework_matches * 2 + database_matches * 2 + tools_matches * 1) / 8
            project_score = project_relevance / 10
            
            # Experience level assessment
            experience_score = self._assess_experience_level(text, profile["seniority"])
            
            # Final weighted score
            final_score = (
                skill_score * profile["skills_weight"] +
                project_score * profile["projects_weight"] +
                experience_score * profile["experience_weight"]
            ) * 100
            
            # HR-like minimum requirements check
            total_skill_matches = core_matches + framework_matches + database_matches + tools_matches
            if total_skill_matches < profile["min_skills"]:
                final_score = max(final_score - 20, 0)
            
            # Bonus for skills diversity
            if len(set(all_skills)) > 10:
                final_score += 5
            
            # Project skills bonus
            if len(project_skills) > 3:
                final_score += 5
            
            final_score = min(int(final_score), 100)
            
            # Generate HR-like assessment
            matching_skills = self._get_matching_skills(all_skills, profile)
            missing_critical = self._get_missing_critical_skills(all_skills, profile)
            hr_assessment = self._generate_hr_assessment(final_score, total_skill_matches, project_relevance, job_title, matching_skills)
            
            job_matches.append({
                "job_title": job_title,
                "match_percentage": final_score,
                "matching_skills": matching_skills,
                "missing_skills": missing_critical,
                "match_reasons": hr_assessment,
                "skill_breakdown": {
                    "core": f"{core_matches}/{len(profile['core_skills'])}",
                    "frameworks": f"{framework_matches}/{len(profile['framework_skills'])}",
                    "databases": f"{database_matches}/{len(profile['database_skills'])}",
                    "tools": f"{tools_matches}/{len(profile['tools_skills'])}"
                },
                "hr_recommendation": self._get_hr_recommendation(final_score, job_title)
            })
        
        # Sort and return top 3 like HR would prioritize
        job_matches.sort(key=lambda x: x["match_percentage"], reverse=True)
        return job_matches[:3]
    
    def _count_skill_matches(self, candidate_skills: List[str], required_skills: List[str]) -> int:
        """Count skill matches with fuzzy matching"""
        matches = 0
        for req_skill in required_skills:
            for cand_skill in candidate_skills:
                if (req_skill.lower() in cand_skill or cand_skill in req_skill.lower() or
                    self._are_similar_skills(req_skill.lower(), cand_skill)):
                    matches += 1
                    break
        return matches
    
    def _are_similar_skills(self, skill1: str, skill2: str) -> bool:
        """Check if skills are similar (e.g., React and React.js)"""
        similar_pairs = [
            ("javascript", "js"), ("typescript", "ts"), ("react", "reactjs"),
            ("node.js", "nodejs"), ("vue.js", "vuejs"), ("angular", "angularjs"),
            ("postgresql", "postgres"), ("mongodb", "mongo")
        ]
        
        for pair in similar_pairs:
            if (skill1 in pair and skill2 in pair) or (skill2 in pair and skill1 in pair):
                return True
        return False
    
    def _analyse_project_relevance(self, text: str, indicators: List[str]) -> int:
        """Analyse how relevant projects are to the job"""
        relevance_score = 0
        for indicator in indicators:
            if re.search(r'\b' + indicator + r'\b', text, re.IGNORECASE):
                relevance_score += 1
        return min(relevance_score, 10)
    
    def _assess_experience_level(self, text: str, required_seniority: str) -> float:
        """Assess experience level from resume"""
        years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        years_matches = re.findall(years_pattern, text, re.IGNORECASE)
        
        max_years = 0
        if years_matches:
            max_years = max(int(year) for year in years_matches)
        
        # Experience scoring
        if required_seniority == "junior":
            return 1.0 if max_years <= 2 else 0.8
        elif required_seniority == "mid":
            return 1.0 if 2 <= max_years <= 5 else 0.7
        elif required_seniority == "senior":
            return 1.0 if max_years >= 5 else 0.6
        
        return 0.7  # Default
    
    def _get_matching_skills(self, candidate_skills: List[str], profile: Dict) -> List[str]:
        """Get all matching skills"""
        all_required = (profile["core_skills"] + profile["framework_skills"] + 
                       profile["database_skills"] + profile["tools_skills"])
        
        matching = []
        for req_skill in all_required:
            for cand_skill in candidate_skills:
                if (req_skill.lower() in cand_skill or cand_skill in req_skill.lower() or
                    self._are_similar_skills(req_skill.lower(), cand_skill)):
                    matching.append(req_skill)
                    break
        
        return list(set(matching))
    
    def _get_missing_critical_skills(self, candidate_skills: List[str], profile: Dict) -> List[str]:
        """Get missing critical skills"""
        critical_skills = profile["core_skills"] + profile["framework_skills"][:2]
        
        missing = []
        for skill in critical_skills:
            found = False
            for cand_skill in candidate_skills:
                if (skill.lower() in cand_skill or cand_skill in skill.lower() or
                    self._are_similar_skills(skill.lower(), cand_skill)):
                    found = True
                    break
            if not found:
                missing.append(skill)
        
        return missing[:5]
    
    def _generate_hr_assessment(self, score: int, skill_matches: int, project_relevance: int, job_title: str, matching_skills: List[str]) -> List[str]:
        """Generate AI-powered personalized assessment for each job role"""
        assessment = []
        
        # Role-specific assessments based on job title and skills
        role_assessments = {
            "Senior Software Engineer": {
                "high": "Demonstrates senior-level expertise with strong architectural and system design capabilities",
                "medium": "Shows solid engineering fundamentals with room for senior-level growth",
                "low": "Has basic programming skills but lacks senior-level system design experience"
            },
            "Full Stack Developer": {
                "high": "Excellent full-stack capabilities spanning frontend, backend, and database technologies",
                "medium": "Good foundation in web development with balanced frontend/backend skills",
                "low": "Limited full-stack experience, stronger in either frontend or backend development"
            },
            "Data Scientist": {
                "high": "Strong analytical skills with proven machine learning and statistical modeling expertise",
                "medium": "Solid data analysis foundation with growing ML/AI capabilities",
                "low": "Basic data skills present but lacks advanced statistical and ML experience"
            },
            "DevOps Engineer": {
                "high": "Comprehensive DevOps expertise in cloud infrastructure, automation, and CI/CD pipelines",
                "medium": "Good understanding of deployment and infrastructure with developing automation skills",
                "low": "Basic infrastructure knowledge but limited experience with advanced DevOps practices"
            },
            "Frontend Developer": {
                "high": "Exceptional UI/UX development skills with modern framework expertise and design sensibility",
                "medium": "Solid frontend development capabilities with good framework knowledge",
                "low": "Basic web development skills but needs growth in modern frontend frameworks"
            },
            "Backend Developer": {
                "high": "Strong server-side development expertise with robust API design and database optimization skills",
                "medium": "Good backend fundamentals with solid API development experience",
                "low": "Basic server-side programming but lacks advanced backend architecture experience"
            },
            "Mobile Developer": {
                "high": "Comprehensive mobile development expertise across platforms with strong app architecture skills",
                "medium": "Good mobile development foundation with platform-specific knowledge",
                "low": "Basic mobile development skills but limited cross-platform experience"
            },
            "Data Engineer": {
                "high": "Excellent data pipeline and ETL expertise with strong big data processing capabilities",
                "medium": "Solid data engineering fundamentals with growing pipeline development skills",
                "low": "Basic data processing knowledge but lacks advanced pipeline architecture experience"
            },
            "Machine Learning Engineer": {
                "high": "Outstanding ML engineering skills with production model deployment and MLOps expertise",
                "medium": "Good ML fundamentals with developing model deployment capabilities",
                "low": "Basic ML knowledge but limited experience in production ML systems"
            },
            "Cloud Architect": {
                "high": "Exceptional cloud architecture expertise with multi-cloud strategy and enterprise-scale design",
                "medium": "Solid cloud platform knowledge with growing architectural design skills",
                "low": "Basic cloud familiarity but lacks comprehensive architectural experience"
            }
        }
        
        # Determine score category
        if score >= 75:
            score_level = "high"
        elif score >= 50:
            score_level = "medium"
        else:
            score_level = "low"
        
        # Get role-specific assessment
        if job_title in role_assessments:
            assessment.append(role_assessments[job_title][score_level])
        else:
            # Fallback generic assessment
            if score >= 75:
                assessment.append("Strong technical alignment with excellent skill match")
            elif score >= 50:
                assessment.append("Good technical foundation with solid skill coverage")
            else:
                assessment.append("Basic technical skills with significant growth potential")
        
        # Add skill-specific insights
        if len(matching_skills) >= 8:
            assessment.append(f"Comprehensive skill portfolio with {len(matching_skills)} relevant technologies")
        elif len(matching_skills) >= 4:
            assessment.append(f"Solid technical skill set covering {len(matching_skills)} key areas")
        elif len(matching_skills) >= 1:
            assessment.append(f"Foundational skills present in {len(matching_skills)} core areas")
        
        # Add project relevance insight
        if project_relevance >= 6:
            assessment.append("Strong project portfolio demonstrates hands-on experience and practical application")
        elif project_relevance >= 3:
            assessment.append("Relevant project experience shows practical skill application")
        
        return assessment
    
    def _get_hr_recommendation(self, score: int, job_title: str) -> str:
        """Get HR recommendation"""
        if score >= 85:
            return f"Highly recommend for {job_title} - excellent fit"
        elif score >= 70:
            return f"Recommend for {job_title} - good candidate"
        elif score >= 55:
            return f"Consider for {job_title} - with some training"
        else:
            return f"Not recommended for {job_title} - significant skill gaps"