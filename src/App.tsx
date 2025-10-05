import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import AnalysisResults from './components/AnalysisResults';
import { AnalysisResult } from './types';

function App() {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalysisComplete = (result: AnalysisResult) => {
    setAnalysisResult(result);
    setLoading(false);
  };

  const handleAnalysisStart = () => {
    setLoading(true);
    setAnalysisResult(null);
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Resume Analyser</h1>
        <p>Upload your resume and get AI-powered job recommendations</p>
      </header>
      
      <main className="App-main">
        {!analysisResult && !loading && (
          <FileUpload 
            onAnalysisStart={handleAnalysisStart}
            onAnalysisComplete={handleAnalysisComplete}
          />
        )}
        
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Analysing your resume...</p>
          </div>
        )}
        
        {analysisResult && (
          <AnalysisResults 
            result={analysisResult}
            onReset={handleReset}
          />
        )}
      </main>
    </div>
  );
}

export default App;
