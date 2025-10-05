import React from 'react';
import { DetectedCategory } from '../types';
import './CategoryDisplay.css';

interface CategoryDisplayProps {
  categories: DetectedCategory[];
}

const CategoryDisplay: React.FC<CategoryDisplayProps> = ({ categories }) => {
  return (
    <div className="detected-categories">
      <h4>🎯 Detected Career Categories</h4>
      <div className="category-matches">
        {categories?.map((category, index) => (
          <div key={index} className="category-match">
            <div className="category-name">{category.category}</div>
            <div className="category-confidence">{category.confidence}% confidence</div>
            <div className={`category-strength ${category.match_strength.toLowerCase()}`}>
              {category.match_strength} Match
            </div>
          </div>
        )) || <p>No categories detected</p>}
      </div>
    </div>
  );
};

export default CategoryDisplay;