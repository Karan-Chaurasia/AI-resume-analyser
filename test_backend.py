#!/usr/bin/env python3
"""
Test script to verify backend functionality
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database.models import init_db, get_job_roles
from database.job_roles import populate_job_roles
from services.resume_parser import ResumeParser
from services.ai_analyzer import AIAnalyzer
from services.job_matcher import JobMatcher

def test_database():
    """Test database initialization and job roles"""
    print("Testing database...")
    init_db()
    populate_job_roles()
    
    roles = get_job_roles()
    print(f"✓ Database initialized with {len(roles)} job roles")
    
    # Print first few roles
    for i, role in enumerate(roles[:3]):
        print(f"  - {role['title']} ({role['category']})")
    
    return True

def test_services():
    """Test service initialization"""
    print("\nTesting services...")
    
    try:
        parser = ResumeParser()
        print("✓ Resume parser initialized")
        
        analyzer = AIAnalyzer()
        print("✓ AI analyzer initialized")
        
        matcher = JobMatcher()
        print("✓ Job matcher initialized")
        
        return True
    except Exception as e:
        print(f"✗ Service initialization failed: {e}")
        return False

def test_sample_analysis():
    """Test with sample resume data"""
    print("\nTesting sample analysis...")
    
    # Sample resume data
    sample_data = {
        'raw_text': 'John Doe Software Engineer with Python and React experience',
        'language': 'en',
        'name': 'John Doe',
        'contact_info': {'email': 'john@example.com'},
        'skills': ['Python', 'React', 'JavaScript', 'SQL'],
        'projects': [
            {
                'title': 'Web Application',
                'description': 'Built a web app using React and Node.js',
                'technologies': ['React', 'Node.js', 'JavaScript']
            }
        ],
        'experience': [
            {
                'title': 'Software Developer',
                'description': 'Developed web applications using modern technologies'
            }
        ],
        'education': []
    }
    
    try:
        analyzer = AIAnalyzer()
        analysis = analyzer.analyze(sample_data)
        print(f"✓ Analysis completed - Compatibility score: {analysis['compatibility_score']}%")
        
        matcher = JobMatcher()
        matches = matcher.find_matches(sample_data, analysis)
        print(f"✓ Found {len(matches)} job matches")
        
        if matches:
            best_match = matches[0]
            print(f"  Best match: {best_match['job_title']} ({best_match['match_percentage']}%)")
        
        return True
    except Exception as e:
        print(f"✗ Analysis failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Resume Analyzer Backend Test")
    print("=" * 40)
    
    tests = [
        test_database,
        test_services,
        test_sample_analysis
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed: {e}")
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Backend is ready.")
    else:
        print("❌ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()