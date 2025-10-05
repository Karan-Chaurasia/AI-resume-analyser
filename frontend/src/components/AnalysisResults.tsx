import React, { useState } from 'react';
import { AnalysisResult } from '../types';
import CategoryDisplay from './CategoryDisplay';
import './AnalysisResults.css';

interface AnalysisResultsProps {
  result: AnalysisResult;
  onReset: () => void;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ result, onReset }) => {
  const [activeTab, setActiveTab] = useState('overview');
  
  const downloadReport = () => {
    const reportData = {
      name: result.extracted_data.name,
      compatibility_score: result.compatibility_score,
      job_matches: result.job_matches,
      suggestions: result.suggestions,
      analysis: result.analysis
    };
    
    const dataStr = JSON.stringify(reportData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = 'resume_analysis_report.json';
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };
  
  return (
    <div className="analysis-results">
      <div className="results-header">
        <h2>Resume Analysis Results</h2>
        <div className="header-actions">
          {result.original_language && result.original_language !== 'en' && (
            <button 
              onClick={() => window.location.reload()} 
              className="translate-btn"
              title="Toggle English Translation"
            >
              🌐 {result.translated_to ? 'Show Original' : 'Translate to English'}
            </button>
          )}
          <button onClick={downloadReport} className="download-btn">
            📥 Download Report
          </button>
          <button onClick={onReset} className="reset-btn">
            🔄 Analyse Another Resume
          </button>
        </div>
      </div>
      
      <div className="candidate-info">
        <h3>👤 {result.extracted_data.name || 'Candidate'}</h3>
        <div className="contact-info">
          {result.extracted_data.contact_info.email && (
            <span>📧 {result.extracted_data.contact_info.email}</span>
          )}
          {result.extracted_data.contact_info.phone && (
            <span>📞 {result.extracted_data.contact_info.phone}</span>
          )}
          {result.extracted_data.contact_info.linkedin && (
            <span>💼 LinkedIn</span>
          )}
        </div>
      </div>
      
      <div className="compatibility-score">
        <h3>Overall Compatibility Score</h3>
        <div className="score-container">
          <div className="score-circle">
            <div className="score-value">{result.compatibility_score}%</div>
          </div>
          <div className="score-description">
            {result.compatibility_score >= 80 ? 'Excellent Match' :
             result.compatibility_score >= 60 ? 'Good Match' :
             result.compatibility_score >= 40 ? 'Fair Match' : 'Needs Improvement'}
          </div>
        </div>
      </div>
      
      <div className="tabs">
        <button 
          className={activeTab === 'overview' ? 'active' : ''}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={activeTab === 'jobs' ? 'active' : ''}
          onClick={() => setActiveTab('jobs')}
        >
          Job Matches
        </button>
        <button 
          className={activeTab === 'skills' ? 'active' : ''}
          onClick={() => setActiveTab('skills')}
        >
          Skills Analysis
        </button>
        <button 
          className={activeTab === 'suggestions' ? 'active' : ''}
          onClick={() => setActiveTab('suggestions')}
        >
          Suggestions
        </button>
      </div>
      
      <div className="tab-content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="stats-grid">
              <div className="stat-card">
                <h4>Skills Found</h4>
                <div className="stat-value">{result.extracted_data.skills.length}</div>
              </div>
              <div className="stat-card">
                <h4>Projects</h4>
                <div className="stat-value">{result.extracted_data.projects.length}</div>
              </div>
              <div className="stat-card">
                <h4>Experience</h4>
                <div className="stat-value">{result.extracted_data.experience.length}</div>
              </div>
              <div className="stat-card">
                <h4>Language</h4>
                <div className="stat-value">{result.extracted_data.language.toUpperCase()}</div>
              </div>
            </div>
            
            <CategoryDisplay categories={result.detected_categories} />
            
            <div className="strengths-weaknesses">
              <div className="strengths">
                <h4>💪 Strengths</h4>
                <ul>
                  {result.analysis.strengths.map((strength, index) => (
                    <li key={index}>{strength}</li>
                  ))}
                </ul>
              </div>
              <div className="weaknesses">
                <h4>⚠️ Areas for Improvement</h4>
                <ul>
                  {result.analysis.weaknesses.map((weakness, index) => (
                    <li key={index}>{weakness}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
        
        {activeTab === 'jobs' && (
          <div className="jobs-tab">
            <h3>🎯 Top Job Matches</h3>
            <div className="job-matches">
              {result.job_matches.map((job, index) => (
                <div key={index} className="job-card">
                  <div className="job-header">
                    <h4>{job.job_title}</h4>
                    <div className="match-percentage">{job.match_percentage}%</div>
                  </div>
                  <p className="job-category">{job.category}</p>
                  
                  <div className="job-details">
                    <div className="matching-skills">
                      <h5>✅ Matching Skills</h5>
                      <div className="skill-tags">
                        {job.matching_skills.map((skill, idx) => (
                          <span key={idx} className="skill-tag matching">{skill}</span>
                        ))}
                      </div>
                    </div>
                    
                    <div className="missing-skills">
                      <h5>❌ Missing Skills</h5>
                      <div className="skill-tags">
                        {job.missing_skills.slice(0, 5).map((skill, idx) => (
                          <span key={idx} className="skill-tag missing">{skill}</span>
                        ))}
                      </div>
                    </div>
                    
                    <div className="match-reasons">
                      <h5>🎯 Why This Matches</h5>
                      <ul>
                        {job.match_reasons.map((reason, idx) => (
                          <li key={idx}>{reason}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'skills' && (
          <div className="skills-tab">
            <div className="skills-overview">
              <h3>🛠️ Skills Analysis</h3>
              <div className="skills-stats">
                <div className="skill-stat">
                  <span>Total Skills: {result.analysis.skill_analysis.total_skills}</span>
                </div>
                <div className="skill-stat">
                  <span>Diversity Score: {result.analysis.skill_analysis.diversity_score}/100</span>
                </div>
              </div>
            </div>
            
            <div className="categorized-skills">
              {Object.entries(result.analysis.skill_analysis.categorized_skills).map(([category, skills]) => (
                <div key={category} className="skill-category">
                  <h4>{category.replace('_', ' ').toUpperCase()}</h4>
                  <div className="skill-tags">
                    {skills.map((skill, idx) => (
                      <span key={idx} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
            
            <div className="projects-section">
              <h3>📁 Projects</h3>
              {result.extracted_data.projects.map((project, index) => (
                <div key={index} className="project-card">
                  <h4>{project.title}</h4>
                  <p>{project.description}</p>
                  <div className="project-technologies">
                    {project.technologies.map((tech, idx) => (
                      <span key={idx} className="tech-tag">{tech}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {activeTab === 'suggestions' && (
          <div className="suggestions-tab">
            <h3>💡 Improvement Suggestions</h3>
            <div className="suggestions-list">
              {result.suggestions.map((suggestion, index) => (
                <div key={index} className="suggestion-card">
                  <div className="suggestion-icon">💡</div>
                  <div className="suggestion-text">{suggestion}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisResults;