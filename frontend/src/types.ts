export interface ContactInfo {
  email?: string;
  phone?: string;
  linkedin?: string;
}

export interface Project {
  title: string;
  description: string;
  technologies: string[];
}

export interface Experience {
  title: string;
  description: string;
}

export interface Education {
  degree: string;
  institution: string;
}

export interface ExtractedData {
  raw_text: string;
  language: string;
  name: string;
  contact_info: ContactInfo;
  skills: string[];
  projects: Project[];
  experience: Experience[];
  education: Education[];
}

export interface SkillAnalysis {
  categorized_skills: Record<string, string[]>;
  total_skills: number;
  diversity_score: number;
}

export interface ProjectAnalysis {
  project_count: number;
  technology_diversity: number;
  complexity_score: number;
  technologies_used: string[];
}

export interface Analysis {
  skill_analysis: SkillAnalysis;
  project_analysis: ProjectAnalysis;
  compatibility_score: number;
  suggestions: string[];
  strengths: string[];
  weaknesses: string[];
}

export interface JobMatch {
  job_title: string;
  category: string;
  similarity_score: number;
  match_percentage: number;
  required_skills: string[];
  matching_skills: string[];
  missing_skills: string[];
  match_reasons: string[];
}

export interface DetectedCategory {
  category: string;
  confidence: number;
  match_strength: string;
}

export interface AnalysisResult {
  extracted_data: ExtractedData;
  analysis: Analysis;
  job_matches: JobMatch[];
  detected_categories: DetectedCategory[];
  compatibility_score: number;
  suggestions: string[];
  original_language?: string;
  translated_to?: string;
}