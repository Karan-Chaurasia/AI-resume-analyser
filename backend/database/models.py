import sqlite3
from typing import List, Dict, Any
import os

DATABASE_PATH = "resume_analyzer.db"

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create job_roles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            required_skills TEXT,  -- JSON string of skills array
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create users table for future authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create analysis_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT,
            analysis_result TEXT,  -- JSON string
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_job_roles() -> List[Dict[str, Any]]:
    """Get all job roles from database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT title, category, description, required_skills FROM job_roles')
    rows = cursor.fetchall()
    
    job_roles = []
    for row in rows:
        title, category, description, required_skills_str = row
        required_skills = required_skills_str.split(',') if required_skills_str else []
        
        job_roles.append({
            'title': title,
            'category': category,
            'description': description,
            'required_skills': required_skills
        })
    
    conn.close()
    return job_roles

def insert_job_role(title: str, category: str, description: str, required_skills: List[str]):
    """Insert a new job role into database"""
    # Input validation
    if not title or len(title) > 200:
        raise ValueError("Invalid title")
    if not category or len(category) > 100:
        raise ValueError("Invalid category")
    if len(description) > 1000:
        raise ValueError("Description too long")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Sanitize skills
    sanitized_skills = [skill[:50] for skill in required_skills if skill.strip()]
    required_skills_str = ','.join(sanitized_skills)
    
    cursor.execute('''
        INSERT INTO job_roles (title, category, description, required_skills)
        VALUES (?, ?, ?, ?)
    ''', (title[:200], category[:100], description[:1000], required_skills_str))
    
    conn.commit()
    conn.close()

def clear_job_roles():
    """Clear all job roles from database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM job_roles')
    conn.commit()
    conn.close()