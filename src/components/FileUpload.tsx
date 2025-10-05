import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { AnalysisResult } from '../types';
import './FileUpload.css';

interface FileUploadProps {
  onAnalysisStart: () => void;
  onAnalysisComplete: (result: AnalysisResult) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onAnalysisStart, onAnalysisComplete }) => {
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    
    const file = acceptedFiles[0];
    
    // File validation
    const maxSize = 10 * 1024 * 1024; // 10MB
    
    if (file.size > maxSize) {
      alert('File size must be less than 10MB');
      return;
    }
    
    if (file.name.length > 255) {
      alert('Filename too long');
      return;
    }
    
    if (!file.name.toLowerCase().endsWith('.pdf') && !file.name.toLowerCase().endsWith('.docx')) {
      alert('Please upload a PDF or DOCX file');
      return;
    }
    
    onAnalysisStart();
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/analyse-resume?translate_to=en`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000,
        maxContentLength: 10 * 1024 * 1024,
      });
      
      onAnalysisComplete(response.data);
    } catch (error) {
      console.error('Error analysing resume:', error);
      alert('Error analysing resume. Please try again.');
    }
  }, [onAnalysisStart, onAnalysisComplete]);
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    multiple: false
  });
  
  return (
    <div className="file-upload-container">
      <div 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="upload-content">
          <div className="upload-icon">📄</div>
          {isDragActive ? (
            <p>Drop your resume here...</p>
          ) : (
            <>
              <p>Drag & drop your resume here, or click to select</p>
              <p className="file-types">Supports PDF and DOCX files</p>
              <button className="upload-button">Choose File</button>
            </>
          )}
        </div>
      </div>
      
      <div className="supported-languages">
        <h3>Supported Languages</h3>
        <div className="language-grid">
          <span>🇺🇸 English</span>
          <span>🇬🇷 Greek</span>
          <span>🇳🇱 Dutch</span>
          <span>🇫🇷 French</span>
          <span>🇩🇪 German</span>
          <span>🇫🇮 Finnish</span>
          <span>🇸🇪 Swedish</span>
          <span>🇻🇳 Vietnamese</span>
          <span>🇸🇦 Arabic</span>
          <span>🇹🇭 Thai</span>
          <span>🇪🇸 Spanish</span>
          <span>🇮🇳 Hindi</span>
          <span>🇹🇷 Turkish</span>
          <span>🇵🇱 Polish</span>
          <span>🇳🇴 Norwegian</span>
          <span>🇰🇷 Korean</span>
          <span>🇵🇹 Portuguese</span>
          <span>🇷🇺 Russian</span>
          <span>🇯🇵 Japanese</span>
          <span>🇨🇳 Chinese</span>
          <span>🇮🇹 Italian</span>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;