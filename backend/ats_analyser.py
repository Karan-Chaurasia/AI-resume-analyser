"""
ATS (Applicant Tracking System) AI Analyzer for precision resume matching
"""
import re
from typing import Dict, List, Tuple
from ai_hr_analyser import AIHRAnalyser

class ATSAnalyser:
    def __init__(self):
        self.hr_analyser = AIHRAnalyser()
        
        # ATS keyword database with weights
        self.ats_keywords = {
            'technical': {
                'python': 10, 'java': 10, 'javascript': 10, 'react': 9, 'angular': 9,
                'node.js': 9, 'sql': 8, 'mongodb': 7, 'aws': 9, 'docker': 8,
                'kubernetes': 8, 'git': 7, 'api': 7, 'rest': 6, 'json': 5
            },
            'soft_skills': {
                'leadership': 8, 'communication': 7, 'teamwork': 7, 'problem solving': 8,
                'analytical': 6, 'creative': 5, 'adaptable': 6, 'organized': 5
            },
            'experience': {
                'senior': 9, 'lead': 8, 'manager': 9, 'architect': 8, 'developer': 7,
                'engineer': 7, 'analyst': 6, 'consultant': 6, 'specialist': 6
            },
            'education': {
                'bachelor': 6, 'master': 8, 'phd': 9, 'mba': 7, 'certification': 5,
                'degree': 5, 'computer science': 8, 'engineering': 7
            }
        }
    
    def analyse_ats_compatibility(self, resume_text: str, job_description: str = "") -> Dict:
        """Comprehensive ATS analysis with AI precision"""
        
        # Extract resume data
        skills = self.hr_analyser._extract_skills_from_text(resume_text)
        
        # ATS keyword matching
        keyword_matches = self._match_ats_keywords(resume_text)
        
        # Format analysis
        format_score = self._analyse_format(resume_text)
        
        # Readability score
        readability_score = self._calculate_readability(resume_text)
        
        # Job matching if job description provided
        job_match_score = 0
        if job_description:
            job_match_score = self._match_job_description(resume_text, job_description)
        
        # Calculate overall ATS score
        ats_score = self._calculate_ats_score(keyword_matches, format_score, readability_score, job_match_score)
        
        return {
            'ats_score': ats_score,
            'keyword_matches': keyword_matches,
            'format_score': format_score,
            'readability_score': readability_score,
            'job_match_score': job_match_score,
            'recommendations': self._generate_ats_recommendations(ats_score, keyword_matches, format_score),
            'missing_keywords': self._find_missing_keywords(resume_text),
            'ats_friendly': ats_score >= 70
        }
    
    def _match_ats_keywords(self, text: str) -> Dict:
        """Match ATS keywords with weighted scoring"""
        matches = {'technical': [], 'soft_skills': [], 'experience': [], 'education': []}
        scores = {'technical': 0, 'soft_skills': 0, 'experience': 0, 'education': 0}
        
        text_lower = text.lower()
        
        for category, keywords in self.ats_keywords.items():
            for keyword, weight in keywords.items():
                if keyword.lower() in text_lower:
                    matches[category].append(keyword)
                    scores[category] += weight
        
        return {
            'matches': matches,
            'scores': scores,
            'total_score': sum(scores.values())
        }
    
    def _analyse_format(self, text: str) -> int:
        """Analyse resume format for ATS compatibility"""
        score = 100
        
        # Check for problematic formatting
        if len(re.findall(r'[^\x00-\x7F]', text)) > 50:  # Too many special characters
            score -= 10
        
        if len(text.split('\n')) < 10:  # Too few line breaks
            score -= 15
        
        if len(re.findall(r'\t', text)) > 20:  # Too many tabs
            score -= 10
        
        # Check for good structure
        if any(section in text.lower() for section in ['experience', 'education', 'skills']):
            score += 10
        
        if re.search(r'\d{4}', text):  # Has years
            score += 5
        
        return max(0, min(100, score))
    
    def _calculate_readability(self, text: str) -> int:
        """Calculate readability score for ATS"""
        words = len(text.split())
        sentences = len(re.findall(r'[.!?]+', text))
        
        if sentences == 0:
            return 50
        
        avg_words_per_sentence = words / sentences
        
        # Optimal range: 15-20 words per sentence
        if 15 <= avg_words_per_sentence <= 20:
            return 100
        elif 10 <= avg_words_per_sentence <= 25:
            return 80
        else:
            return 60
    
    def _match_job_description(self, resume_text: str, job_description: str) -> int:
        """Match resume against job description"""
        resume_words = set(resume_text.lower().split())
        job_words = set(job_description.lower().split())
        
        # Filter meaningful words (length > 3)
        resume_words = {word for word in resume_words if len(word) > 3}
        job_words = {word for word in job_words if len(word) > 3}
        
        if not job_words:
            return 0
        
        matches = resume_words.intersection(job_words)
        match_percentage = (len(matches) / len(job_words)) * 100
        
        return min(100, int(match_percentage))
    
    def _calculate_ats_score(self, keyword_matches: Dict, format_score: int, readability_score: int, job_match_score: int) -> int:
        """Calculate overall ATS compatibility score"""
        
        # Weighted scoring
        keyword_weight = 0.4
        format_weight = 0.3
        readability_weight = 0.2
        job_match_weight = 0.1
        
        # Normalize keyword score (max possible: ~200)
        keyword_score = min(100, (keyword_matches['total_score'] / 200) * 100)
        
        total_score = (
            keyword_score * keyword_weight +
            format_score * format_weight +
            readability_score * readability_weight +
            job_match_score * job_match_weight
        )
        
        return int(total_score)
    
    def _generate_ats_recommendations(self, ats_score: int, keyword_matches: Dict, format_score: int) -> List[str]:
        """Generate ATS improvement recommendations"""
        recommendations = []
        
        if ats_score < 70:
            recommendations.append("Improve overall ATS compatibility - score below 70%")
        
        if keyword_matches['scores']['technical'] < 30:
            recommendations.append("Add more technical keywords relevant to your field")
        
        if keyword_matches['scores']['soft_skills'] < 20:
            recommendations.append("Include soft skills like leadership, communication, teamwork")
        
        if format_score < 80:
            recommendations.append("Improve resume formatting - use standard sections and clear structure")
        
        if len(keyword_matches['matches']['experience']) < 3:
            recommendations.append("Include more experience-related keywords (senior, lead, manager)")
        
        return recommendations
    
    def _find_missing_keywords(self, text: str) -> List[str]:
        """Find commonly missing ATS keywords"""
        text_lower = text.lower()
        missing = []
        
        # Common high-value keywords often missing
        important_keywords = [
            'leadership', 'management', 'project management', 'team lead',
            'problem solving', 'analytical', 'communication', 'collaboration',
            'agile', 'scrum', 'ci/cd', 'devops', 'cloud', 'api'
        ]
        
        for keyword in important_keywords:
            if keyword not in text_lower:
                missing.append(keyword)
        
        return missing[:10]  # Return top 10 missing keywords
    
    def scan_for_ats_issues(self, text: str) -> Dict:
        """Scan for specific ATS parsing issues"""
        issues = []
        
        # Check for graphics/tables
        if '|' in text and text.count('|') > 10:
            issues.append("Contains table formatting that may not parse correctly")
        
        # Check for special characters
        special_chars = len(re.findall(r'[^\w\s\-.,()@/:]', text))
        if special_chars > 20:
            issues.append("Contains many special characters that may cause parsing errors")
        
        # Check for contact info
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            issues.append("Missing email address")
        
        if not re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text):
            issues.append("Missing phone number")
        
        return {
            'issues_found': len(issues),
            'issues': issues,
            'ats_friendly': len(issues) < 3
        }