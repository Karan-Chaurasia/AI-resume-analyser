from typing import Dict, List, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from database.models import get_job_roles
from .category_detector import CategoryDetector

class JobMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.job_roles = None
        self.category_detector = CategoryDetector()
        self._load_job_roles()
    
    def _load_job_roles(self):
        self.job_roles = get_job_roles()
    
    def find_matches(self, parsed_data: Dict[str, Any], analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not self.job_roles:
            self._load_job_roles()
        
        # Detect candidate's likely categories
        top_categories = self.category_detector.get_top_categories(
            parsed_data.get('skills', []),
            parsed_data.get('projects', []),
            parsed_data.get('experience', [])
        )
        
        candidate_profile = self._create_candidate_profile(parsed_data)
        matches = []
        
        for job_role in self.job_roles:
            similarity_score = self._calculate_similarity(candidate_profile, job_role)
            
            # Boost score if job category matches detected categories
            category_boost = 0
            for cat_info in top_categories:
                if cat_info['category'] == job_role['category']:
                    category_boost = cat_info['confidence'] / 100 * 0.3  # Up to 30% boost
                    break
            
            final_score = min(similarity_score + category_boost, 1.0)
            match_reasons = self._generate_match_reasons(parsed_data, job_role)
            
            matches.append({
                'job_title': job_role['title'],
                'category': job_role['category'],
                'similarity_score': final_score,
                'match_percentage': int(final_score * 100),
                'required_skills': job_role['required_skills'],
                'matching_skills': self._find_matching_skills(parsed_data['skills'], job_role['required_skills']),
                'missing_skills': self._find_missing_skills(parsed_data['skills'], job_role['required_skills']),
                'match_reasons': match_reasons,
                'category_match': category_boost > 0
            })
        
        # Sort by final score and return top 3
        matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        return matches[:3]
    
    def _create_candidate_profile(self, parsed_data: Dict[str, Any]) -> str:
        profile_parts = []
        
        # Add skills
        skills = parsed_data.get('skills', [])
        if skills:
            profile_parts.append(' '.join(skills))
        
        # Add project technologies
        projects = parsed_data.get('projects', [])
        for project in projects:
            technologies = project.get('technologies', [])
            profile_parts.extend(technologies)
            
            # Add project description keywords
            description = project.get('description', '')
            profile_parts.append(description)
        
        # Add experience descriptions
        experience = parsed_data.get('experience', [])
        for exp in experience:
            description = exp.get('description', '')
            profile_parts.append(description)
        
        return ' '.join(profile_parts).lower()
    
    def _calculate_similarity(self, candidate_profile: str, job_role: Dict[str, Any]) -> float:
        job_profile = self._create_job_profile(job_role)
        
        try:
            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([candidate_profile, job_profile])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            # Fallback to simple keyword matching
            return self._simple_keyword_match(candidate_profile, job_role)
    
    def _create_job_profile(self, job_role: Dict[str, Any]) -> str:
        profile_parts = []
        
        # Add required skills
        required_skills = job_role.get('required_skills', [])
        profile_parts.extend(required_skills)
        
        # Add job description
        description = job_role.get('description', '')
        profile_parts.append(description)
        
        # Add category
        category = job_role.get('category', '')
        profile_parts.append(category)
        
        return ' '.join(profile_parts).lower()
    
    def _simple_keyword_match(self, candidate_profile: str, job_role: Dict[str, Any]) -> float:
        required_skills = job_role.get('required_skills', [])
        if not required_skills:
            return 0.0
        
        matches = 0
        for skill in required_skills:
            if skill.lower() in candidate_profile:
                matches += 1
        
        return matches / len(required_skills)
    
    def _find_matching_skills(self, candidate_skills: List[str], required_skills: List[str]) -> List[str]:
        matching = []
        candidate_skills_lower = [skill.lower() for skill in candidate_skills]
        
        for req_skill in required_skills:
            for cand_skill in candidate_skills:
                if req_skill.lower() in cand_skill.lower() or cand_skill.lower() in req_skill.lower():
                    matching.append(cand_skill)
                    break
        
        return list(set(matching))
    
    def _find_missing_skills(self, candidate_skills: List[str], required_skills: List[str]) -> List[str]:
        candidate_skills_lower = [skill.lower() for skill in candidate_skills]
        missing = []
        
        for req_skill in required_skills:
            found = False
            for cand_skill in candidate_skills_lower:
                if req_skill.lower() in cand_skill or cand_skill in req_skill.lower():
                    found = True
                    break
            if not found:
                missing.append(req_skill)
        
        return missing
    
    def _generate_match_reasons(self, parsed_data: Dict[str, Any], job_role: Dict[str, Any]) -> List[str]:
        reasons = []
        
        matching_skills = self._find_matching_skills(parsed_data['skills'], job_role['required_skills'])
        if matching_skills:
            reasons.append(f"Strong match in skills: {', '.join(matching_skills[:3])}")
        
        # Check project relevance
        projects = parsed_data.get('projects', [])
        relevant_projects = 0
        for project in projects:
            technologies = project.get('technologies', [])
            if any(tech.lower() in ' '.join(job_role['required_skills']).lower() for tech in technologies):
                relevant_projects += 1
        
        if relevant_projects > 0:
            reasons.append(f"Relevant project experience ({relevant_projects} projects)")
        
        # Check category alignment
        category = job_role.get('category', '').lower()
        candidate_profile = self._create_candidate_profile(parsed_data)
        if category in candidate_profile:
            reasons.append(f"Experience aligns with {job_role['category']} field")
        
        return reasons[:3]  # Limit to top 3 reasons
    
    def get_all_roles(self) -> List[Dict[str, Any]]:
        if not self.job_roles:
            self._load_job_roles()
        return self.job_roles
    
    def get_detected_categories(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get categories detected from candidate's profile"""
        return self.category_detector.get_top_categories(
            parsed_data.get('skills', []),
            parsed_data.get('projects', []),
            parsed_data.get('experience', [])
        )