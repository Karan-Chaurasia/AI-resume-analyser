from typing import Dict, List, Any
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class AIAnalyzer:
    def __init__(self):
        self.skill_categories = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'kotlin', 'swift'],
            'web_development': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask'],
            'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
            'data_science': ['machine learning', 'ai', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn'],
            'mobile': ['android', 'ios', 'react native', 'flutter', 'xamarin'],
            'devops': ['git', 'jenkins', 'ci/cd', 'linux', 'bash', 'terraform']
        }
    
    def analyze(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        skills = parsed_data.get('skills', [])
        projects = parsed_data.get('projects', [])
        experience = parsed_data.get('experience', [])
        
        # Analyze skill distribution
        skill_analysis = self._analyze_skills(skills)
        
        # Analyze projects
        project_analysis = self._analyze_projects(projects)
        
        # Calculate compatibility score
        compatibility_score = self._calculate_compatibility_score(skills, projects, experience)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(parsed_data, skill_analysis)
        
        return {
            'skill_analysis': skill_analysis,
            'project_analysis': project_analysis,
            'compatibility_score': compatibility_score,
            'suggestions': suggestions,
            'strengths': self._identify_strengths(skills, projects),
            'weaknesses': self._identify_weaknesses(skill_analysis)
        }
    
    def _analyze_skills(self, skills: List[str]) -> Dict[str, Any]:
        categorized_skills = {}
        skill_count = 0
        
        for category, category_skills in self.skill_categories.items():
            found_skills = []
            for skill in skills:
                if any(cat_skill.lower() in skill.lower() for cat_skill in category_skills):
                    found_skills.append(skill)
            
            if found_skills:
                categorized_skills[category] = found_skills
                skill_count += len(found_skills)
        
        return {
            'categorized_skills': categorized_skills,
            'total_skills': skill_count,
            'diversity_score': len(categorized_skills) * 10  # Simple diversity metric
        }
    
    def _analyze_projects(self, projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not projects:
            return {'project_count': 0, 'technology_diversity': 0, 'complexity_score': 0}
        
        all_technologies = []
        complexity_indicators = ['api', 'database', 'machine learning', 'ai', 'cloud', 'microservices']
        complexity_score = 0
        
        for project in projects:
            technologies = project.get('technologies', [])
            all_technologies.extend(technologies)
            
            description = project.get('description', '').lower()
            for indicator in complexity_indicators:
                if indicator in description:
                    complexity_score += 10
        
        unique_technologies = list(set(all_technologies))
        
        return {
            'project_count': len(projects),
            'technology_diversity': len(unique_technologies),
            'complexity_score': min(complexity_score, 100),
            'technologies_used': unique_technologies
        }
    
    def _calculate_compatibility_score(self, skills: List[str], projects: List[Dict], experience: List[Dict]) -> int:
        score = 0
        
        # Skills contribution (40%)
        skill_score = min(len(skills) * 5, 40)
        score += skill_score
        
        # Projects contribution (35%)
        project_score = min(len(projects) * 7, 35)
        score += project_score
        
        # Experience contribution (25%)
        experience_score = min(len(experience) * 5, 25)
        score += experience_score
        
        return min(score, 100)
    
    def _generate_suggestions(self, parsed_data: Dict, skill_analysis: Dict) -> List[str]:
        suggestions = []
        
        # Check for missing contact info
        contact = parsed_data.get('contact_info', {})
        if not contact.get('email'):
            suggestions.append("Add a professional email address")
        if not contact.get('linkedin'):
            suggestions.append("Include LinkedIn profile URL")
        
        # Check skills diversity
        if skill_analysis['diversity_score'] < 30:
            suggestions.append("Consider adding skills from different technology categories")
        
        # Check projects
        projects = parsed_data.get('projects', [])
        if len(projects) < 2:
            suggestions.append("Add more project examples to showcase your experience")
        
        # Check for project descriptions
        for project in projects:
            if len(project.get('description', '')) < 50:
                suggestions.append(f"Expand description for project: {project.get('title', 'Untitled')}")
        
        return suggestions
    
    def _identify_strengths(self, skills: List[str], projects: List[Dict]) -> List[str]:
        strengths = []
        
        if len(skills) > 10:
            strengths.append("Strong technical skill set")
        
        if len(projects) > 3:
            strengths.append("Good project portfolio")
        
        # Check for modern technologies
        modern_tech = ['react', 'node.js', 'docker', 'kubernetes', 'aws', 'machine learning']
        if any(tech.lower() in ' '.join(skills).lower() for tech in modern_tech):
            strengths.append("Experience with modern technologies")
        
        return strengths
    
    def _identify_weaknesses(self, skill_analysis: Dict) -> List[str]:
        weaknesses = []
        
        if skill_analysis['total_skills'] < 5:
            weaknesses.append("Limited technical skills listed")
        
        if skill_analysis['diversity_score'] < 20:
            weaknesses.append("Skills concentrated in few areas")
        
        categories = skill_analysis['categorized_skills']
        if 'cloud' not in categories:
            weaknesses.append("No cloud platform experience mentioned")
        
        if 'databases' not in categories:
            weaknesses.append("No database experience mentioned")
        
        return weaknesses