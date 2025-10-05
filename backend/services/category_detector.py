from typing import Dict, List, Set
from collections import defaultdict

class CategoryDetector:
    def __init__(self):
        self.skill_to_categories = {
            # Software & IT
            'python': ['Software & IT'],
            'java': ['Software & IT'],
            'javascript': ['Software & IT'],
            'react': ['Software & IT'],
            'node.js': ['Software & IT'],
            'angular': ['Software & IT'],
            'vue.js': ['Software & IT'],
            'html': ['Software & IT'],
            'css': ['Software & IT'],
            'sql': ['Software & IT'],
            'mongodb': ['Software & IT'],
            'postgresql': ['Software & IT'],
            'mysql': ['Software & IT'],
            'docker': ['Software & IT'],
            'kubernetes': ['Software & IT'],
            'aws': ['Software & IT'],
            'azure': ['Software & IT'],
            'gcp': ['Software & IT'],
            'git': ['Software & IT'],
            'linux': ['Software & IT'],
            'machine learning': ['Software & IT'],
            'ai': ['Software & IT'],
            'tensorflow': ['Software & IT'],
            'pytorch': ['Software & IT'],
            'data science': ['Software & IT'],
            'cybersecurity': ['Software & IT'],
            'network security': ['Software & IT'],
            'devops': ['Software & IT'],
            'ci/cd': ['Software & IT'],
            
            # Engineering
            'autocad': ['Engineering'],
            'solidworks': ['Engineering'],
            'matlab': ['Engineering', 'Software & IT'],
            'cad': ['Engineering'],
            'civil 3d': ['Engineering'],
            'structural analysis': ['Engineering'],
            'thermodynamics': ['Engineering'],
            'materials science': ['Engineering'],
            'circuit design': ['Engineering'],
            'plc': ['Engineering'],
            'power systems': ['Engineering'],
            'control systems': ['Engineering'],
            'mechanical design': ['Engineering'],
            'electrical design': ['Engineering'],
            
            # Finance & Business
            'excel': ['Finance & Business'],
            'financial modeling': ['Finance & Business'],
            'accounting': ['Finance & Business'],
            'bloomberg': ['Finance & Business'],
            'project management': ['Finance & Business'],
            'agile': ['Finance & Business', 'Software & IT'],
            'scrum': ['Finance & Business', 'Software & IT'],
            'business analysis': ['Finance & Business'],
            'risk management': ['Finance & Business'],
            'financial analysis': ['Finance & Business'],
            
            # Marketing & Customer
            'seo': ['Marketing & Customer'],
            'sem': ['Marketing & Customer'],
            'google analytics': ['Marketing & Customer'],
            'social media': ['Marketing & Customer'],
            'content marketing': ['Marketing & Customer'],
            'email marketing': ['Marketing & Customer'],
            'digital marketing': ['Marketing & Customer'],
            'marketing': ['Marketing & Customer'],
            'crm': ['Marketing & Customer'],
            'salesforce': ['Marketing & Customer'],
            
            # Creative & Design
            'photoshop': ['Creative & Design'],
            'illustrator': ['Creative & Design'],
            'indesign': ['Creative & Design'],
            'figma': ['Creative & Design'],
            'adobe xd': ['Creative & Design'],
            'sketch': ['Creative & Design'],
            'after effects': ['Creative & Design'],
            'premiere': ['Creative & Design'],
            'final cut pro': ['Creative & Design'],
            'ui/ux': ['Creative & Design'],
            'graphic design': ['Creative & Design'],
            'video editing': ['Creative & Design'],
            
            # Manufacturing & Logistics
            'lean manufacturing': ['Manufacturing & Logistics'],
            'six sigma': ['Manufacturing & Logistics'],
            'supply chain': ['Manufacturing & Logistics'],
            'logistics': ['Manufacturing & Logistics'],
            'inventory management': ['Manufacturing & Logistics'],
            'erp': ['Manufacturing & Logistics'],
            'quality control': ['Manufacturing & Logistics'],
            'process improvement': ['Manufacturing & Logistics'],
            
            # Education
            'teaching': ['Education'],
            'curriculum development': ['Education'],
            'instructional design': ['Education'],
            'e-learning': ['Education'],
            'training': ['Education'],
            'mentoring': ['Education'],
            
            # Sustainability
            'sustainability': ['Sustainability & Others'],
            'environmental science': ['Sustainability & Others'],
            'renewable energy': ['Sustainability & Others'],
            'climate analysis': ['Sustainability & Others']
        }
    
    def detect_categories(self, skills: List[str], projects: List[Dict], experience: List[Dict]) -> Dict[str, float]:
        """Detect likely job categories based on skills, projects, and experience"""
        category_scores = defaultdict(float)
        
        # Analyze skills
        for skill in skills:
            skill_lower = skill.lower()
            for skill_key, categories in self.skill_to_categories.items():
                if skill_key in skill_lower or skill_lower in skill_key:
                    for category in categories:
                        category_scores[category] += 1.0
        
        # Analyze project technologies and descriptions
        for project in projects:
            technologies = project.get('technologies', [])
            description = project.get('description', '').lower()
            
            for tech in technologies:
                tech_lower = tech.lower()
                for skill_key, categories in self.skill_to_categories.items():
                    if skill_key in tech_lower or tech_lower in skill_key:
                        for category in categories:
                            category_scores[category] += 0.8
            
            # Check description for category keywords
            for skill_key, categories in self.skill_to_categories.items():
                if skill_key in description:
                    for category in categories:
                        category_scores[category] += 0.5
        
        # Analyze experience descriptions
        for exp in experience:
            description = exp.get('description', '').lower()
            title = exp.get('title', '').lower()
            
            for skill_key, categories in self.skill_to_categories.items():
                if skill_key in description or skill_key in title:
                    for category in categories:
                        category_scores[category] += 0.6
        
        # Normalize scores
        if category_scores:
            max_score = max(category_scores.values())
            for category in category_scores:
                category_scores[category] = category_scores[category] / max_score
        
        return dict(category_scores)
    
    def get_top_categories(self, skills: List[str], projects: List[Dict], experience: List[Dict], top_n: int = 3) -> List[Dict[str, any]]:
        """Get top N categories with scores"""
        category_scores = self.detect_categories(skills, projects, experience)
        
        # Sort by score and return top N
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {
                'category': category,
                'confidence': round(score * 100, 1),
                'match_strength': 'Strong' if score > 0.7 else 'Moderate' if score > 0.4 else 'Weak'
            }
            for category, score in sorted_categories[:top_n]
        ]