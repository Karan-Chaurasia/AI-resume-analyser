from .models import insert_job_role, clear_job_roles, get_job_roles

def populate_job_roles():
    """Populate database with predefined job roles"""
    # Check if already populated
    existing_roles = get_job_roles()
    if existing_roles:
        return
    
    job_roles_data = [
        # Engineering
        {
            'title': 'Software Engineer',
            'category': 'Software & IT',
            'description': 'Design, develop, and maintain software applications',
            'required_skills': ['Python', 'Java', 'JavaScript', 'Git', 'SQL', 'Problem Solving']
        },
        {
            'title': 'Full-Stack Developer',
            'category': 'Software & IT',
            'description': 'Develop both frontend and backend components of web applications',
            'required_skills': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'SQL', 'Git']
        },
        {
            'title': 'Data Scientist',
            'category': 'Software & IT',
            'description': 'Analyze complex data to help companies make better decisions',
            'required_skills': ['Python', 'R', 'Machine Learning', 'Statistics', 'SQL', 'Pandas', 'NumPy']
        },
        {
            'title': 'DevOps Engineer',
            'category': 'Software & IT',
            'description': 'Manage infrastructure and deployment pipelines',
            'required_skills': ['Docker', 'Kubernetes', 'AWS', 'Linux', 'Git', 'CI/CD', 'Terraform']
        },
        {
            'title': 'Mobile App Developer',
            'category': 'Software & IT',
            'description': 'Develop mobile applications for iOS and Android platforms',
            'required_skills': ['Swift', 'Kotlin', 'React Native', 'Flutter', 'iOS', 'Android']
        },
        {
            'title': 'AI/ML Engineer',
            'category': 'Software & IT',
            'description': 'Develop and deploy machine learning models and AI systems',
            'required_skills': ['Python', 'TensorFlow', 'PyTorch', 'Machine Learning', 'Deep Learning', 'Statistics']
        },
        {
            'title': 'Cloud Solutions Architect',
            'category': 'Software & IT',
            'description': 'Design and implement cloud-based solutions',
            'required_skills': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Microservices', 'Architecture']
        },
        {
            'title': 'Cybersecurity Analyst',
            'category': 'Software & IT',
            'description': 'Protect organizations from cyber threats and security breaches',
            'required_skills': ['Network Security', 'Penetration Testing', 'SIEM', 'Incident Response', 'Risk Assessment']
        },
        {
            'title': 'UX/UI Designer',
            'category': 'Creative & Design',
            'description': 'Design user interfaces and user experiences for digital products',
            'required_skills': ['Figma', 'Adobe XD', 'Sketch', 'Prototyping', 'User Research', 'HTML', 'CSS']
        },
        {
            'title': 'Web Developer',
            'category': 'Software & IT',
            'description': 'Build and maintain websites and web applications',
            'required_skills': ['HTML', 'CSS', 'JavaScript', 'React', 'Vue.js', 'PHP', 'WordPress']
        },
        
        # Engineering (Traditional)
        {
            'title': 'Mechanical Engineer',
            'category': 'Engineering',
            'description': 'Design and develop mechanical systems and products',
            'required_skills': ['CAD', 'SolidWorks', 'AutoCAD', 'MATLAB', 'Thermodynamics', 'Materials Science']
        },
        {
            'title': 'Civil Engineer',
            'category': 'Engineering',
            'description': 'Design and oversee construction of infrastructure projects',
            'required_skills': ['AutoCAD', 'Civil 3D', 'Structural Analysis', 'Project Management', 'Construction']
        },
        {
            'title': 'Electrical Engineer',
            'category': 'Engineering',
            'description': 'Design and develop electrical systems and components',
            'required_skills': ['Circuit Design', 'MATLAB', 'PLC', 'Power Systems', 'Electronics', 'Control Systems']
        },
        {
            'title': 'Chemical Engineer',
            'category': 'Engineering',
            'description': 'Design processes for manufacturing chemicals and materials',
            'required_skills': ['Process Design', 'MATLAB', 'Chemical Processes', 'Safety', 'Quality Control']
        },
        
        # Business & Finance
        {
            'title': 'Business Analyst',
            'category': 'Finance & Business',
            'description': 'Analyze business processes and recommend improvements',
            'required_skills': ['Excel', 'SQL', 'Data Analysis', 'Requirements Gathering', 'Process Mapping']
        },
        {
            'title': 'Financial Analyst',
            'category': 'Finance & Business',
            'description': 'Analyze financial data to guide business decisions',
            'required_skills': ['Excel', 'Financial Modeling', 'Accounting', 'Statistics', 'Bloomberg', 'SQL']
        },
        {
            'title': 'Project Manager',
            'category': 'Finance & Business',
            'description': 'Plan, execute, and oversee projects from start to finish',
            'required_skills': ['Project Management', 'Agile', 'Scrum', 'Risk Management', 'Communication', 'Leadership']
        },
        {
            'title': 'Product Manager',
            'category': 'Marketing & Customer',
            'description': 'Guide product development from conception to launch',
            'required_skills': ['Product Strategy', 'Market Research', 'Agile', 'Analytics', 'Communication', 'Leadership']
        },
        
        # Marketing & Customer
        {
            'title': 'Digital Marketing Specialist',
            'category': 'Marketing & Customer',
            'description': 'Develop and execute digital marketing campaigns',
            'required_skills': ['SEO', 'SEM', 'Google Analytics', 'Social Media', 'Content Marketing', 'Email Marketing']
        },
        {
            'title': 'Content Marketing Manager',
            'category': 'Marketing & Customer',
            'description': 'Create and manage content marketing strategies',
            'required_skills': ['Content Strategy', 'SEO', 'Social Media', 'Analytics', 'Writing', 'Marketing']
        },
        {
            'title': 'Social Media Manager',
            'category': 'Marketing & Customer',
            'description': 'Manage social media presence and engagement',
            'required_skills': ['Social Media', 'Content Creation', 'Analytics', 'Community Management', 'Marketing']
        },
        
        # Education
        {
            'title': 'Software Engineering Teacher',
            'category': 'Education',
            'description': 'Teach software engineering concepts and programming',
            'required_skills': ['Teaching', 'Programming', 'Curriculum Development', 'Communication', 'Mentoring']
        },
        {
            'title': 'Data Science Instructor',
            'category': 'Education',
            'description': 'Teach data science and analytics concepts',
            'required_skills': ['Teaching', 'Data Science', 'Statistics', 'Python', 'R', 'Communication']
        },
        
        # Manufacturing & Logistics
        {
            'title': 'Manufacturing Engineer',
            'category': 'Manufacturing & Logistics',
            'description': 'Optimize manufacturing processes and systems',
            'required_skills': ['Lean Manufacturing', 'Six Sigma', 'Process Improvement', 'Quality Control', 'CAD']
        },
        {
            'title': 'Supply Chain Manager',
            'category': 'Manufacturing & Logistics',
            'description': 'Manage supply chain operations and logistics',
            'required_skills': ['Supply Chain', 'Logistics', 'Inventory Management', 'ERP', 'Analytics', 'Negotiation']
        },
        
        # Creative & Design
        {
            'title': 'Graphic Designer',
            'category': 'Creative & Design',
            'description': 'Create visual content for various media',
            'required_skills': ['Adobe Creative Suite', 'Photoshop', 'Illustrator', 'InDesign', 'Typography', 'Branding']
        },
        {
            'title': 'Video Editor',
            'category': 'Creative & Design',
            'description': 'Edit and produce video content',
            'required_skills': ['Adobe Premiere', 'After Effects', 'Final Cut Pro', 'Video Production', 'Storytelling']
        },
        
        # Sustainability & Others
        {
            'title': 'Sustainability Consultant',
            'category': 'Sustainability & Others',
            'description': 'Help organizations implement sustainable practices',
            'required_skills': ['Sustainability', 'Environmental Science', 'Data Analysis', 'Consulting', 'Reporting']
        }
    ]
    
    # Insert all job roles
    for job_role in job_roles_data:
        insert_job_role(
            job_role['title'],
            job_role['category'],
            job_role['description'],
            job_role['required_skills']
        )