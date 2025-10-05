TRANSLATIONS = {
    "es": {
        "Programming Languages": "Lenguajes de Programación",
        "Web Technologies": "Tecnologías Web", 
        "Databases": "Bases de Datos",
        "Cloud & DevOps": "Nube y DevOps",
        "AI & Machine Learning": "IA y Aprendizaje Automático",
        "Mobile Development": "Desarrollo Móvil",
        "Design & UI/UX": "Diseño y UI/UX",
        "Project Management": "Gestión de Proyectos",
        "Software Developer": "Desarrollador de Software",
        "Data Scientist": "Científico de Datos", 
        "DevOps Engineer": "Ingeniero DevOps",
        "Full Stack Developer": "Desarrollador Full Stack",
        "Mobile Developer": "Desarrollador Móvil",
        "Strong expertise in": "Fuerte experiencia en",
        "Good foundation in": "Buena base en",
        "Limited experience in": "Experiencia limitada en",
        "Could expand technical skill set": "Podría ampliar el conjunto de habilidades técnicas",
        "Learn cloud platforms": "Aprender plataformas en la nube",
        "Consider learning AI/ML": "Considerar aprender IA/ML",
        "Add certifications": "Agregar certificaciones"
    },
    "fr": {
        "Programming Languages": "Langages de Programmation",
        "Web Technologies": "Technologies Web",
        "Databases": "Bases de Données", 
        "Cloud & DevOps": "Cloud et DevOps",
        "AI & Machine Learning": "IA et Apprentissage Automatique",
        "Mobile Development": "Développement Mobile",
        "Design & UI/UX": "Design et UI/UX",
        "Project Management": "Gestion de Projet",
        "Software Developer": "Développeur Logiciel",
        "Data Scientist": "Scientifique des Données",
        "DevOps Engineer": "Ingénieur DevOps", 
        "Full Stack Developer": "Développeur Full Stack",
        "Mobile Developer": "Développeur Mobile",
        "Strong expertise in": "Forte expertise en",
        "Good foundation in": "Bonne base en",
        "Limited experience in": "Expérience limitée en",
        "Could expand technical skill set": "Pourrait élargir l'ensemble des compétences techniques",
        "Learn cloud platforms": "Apprendre les plateformes cloud",
        "Consider learning AI/ML": "Envisager d'apprendre l'IA/ML",
        "Add certifications": "Ajouter des certifications"
    },
    "de": {
        "Programming Languages": "Programmiersprachen",
        "Web Technologies": "Web-Technologien",
        "Databases": "Datenbanken",
        "Cloud & DevOps": "Cloud und DevOps", 
        "AI & Machine Learning": "KI und Maschinelles Lernen",
        "Mobile Development": "Mobile Entwicklung",
        "Design & UI/UX": "Design und UI/UX",
        "Project Management": "Projektmanagement",
        "Software Developer": "Software-Entwickler",
        "Data Scientist": "Datenwissenschaftler",
        "DevOps Engineer": "DevOps-Ingenieur",
        "Full Stack Developer": "Full-Stack-Entwickler", 
        "Mobile Developer": "Mobile Entwickler",
        "Strong expertise in": "Starke Expertise in",
        "Good foundation in": "Gute Grundlage in",
        "Limited experience in": "Begrenzte Erfahrung in",
        "Could expand technical skill set": "Könnte technische Fähigkeiten erweitern",
        "Learn cloud platforms": "Cloud-Plattformen lernen",
        "Consider learning AI/ML": "KI/ML lernen erwägen",
        "Add certifications": "Zertifizierungen hinzufügen"
    },
    "zh": {
        "Programming Languages": "编程语言",
        "Web Technologies": "网络技术",
        "Databases": "数据库",
        "Cloud & DevOps": "云计算与运维",
        "AI & Machine Learning": "人工智能与机器学习", 
        "Mobile Development": "移动开发",
        "Design & UI/UX": "设计与用户体验",
        "Project Management": "项目管理",
        "Software Developer": "软件开发工程师",
        "Data Scientist": "数据科学家",
        "DevOps Engineer": "运维工程师",
        "Full Stack Developer": "全栈开发工程师",
        "Mobile Developer": "移动开发工程师",
        "Strong expertise in": "在以下方面有强大的专业知识",
        "Good foundation in": "在以下方面有良好的基础",
        "Limited experience in": "在以下方面经验有限",
        "Could expand technical skill set": "可以扩展技术技能组合",
        "Learn cloud platforms": "学习云平台",
        "Consider learning AI/ML": "考虑学习人工智能/机器学习",
        "Add certifications": "添加认证"
    },
    "ja": {
        "Programming Languages": "プログラミング言語",
        "Web Technologies": "ウェブ技術",
        "Databases": "データベース",
        "Cloud & DevOps": "クラウドとDevOps",
        "AI & Machine Learning": "AIと機械学習",
        "Mobile Development": "モバイル開発", 
        "Design & UI/UX": "デザインとUI/UX",
        "Project Management": "プロジェクト管理",
        "Software Developer": "ソフトウェア開発者",
        "Data Scientist": "データサイエンティスト",
        "DevOps Engineer": "DevOpsエンジニア",
        "Full Stack Developer": "フルスタック開発者",
        "Mobile Developer": "モバイル開発者",
        "Strong expertise in": "以下の分野で強い専門知識",
        "Good foundation in": "以下の分野で良い基盤",
        "Limited experience in": "以下の分野で限られた経験",
        "Could expand technical skill set": "技術スキルセットを拡張できます",
        "Learn cloud platforms": "クラウドプラットフォームを学ぶ",
        "Consider learning AI/ML": "AI/MLの学習を検討する",
        "Add certifications": "認定資格を追加する"
    }
}

def translate_text(text: str, language: str) -> str:
    if language == "en" or language not in TRANSLATIONS:
        return text
    
    translations = TRANSLATIONS[language]
    for english, translated in translations.items():
        if english in text:
            text = text.replace(english, translated)
    
    return text

def translate_to_english(text: str, language: str) -> str:
    if language == "en" or language not in TRANSLATIONS:
        return text
    
    translations = TRANSLATIONS[language]
    for english, translated in translations.items():
        if translated in text:
            text = text.replace(translated, english)
    
    return text