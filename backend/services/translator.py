from googletrans import Translator
from typing import Dict, Any, List
import time
import html

class TranslationService:
    def __init__(self):
        self.translator = Translator()
        self.supported_languages = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'ko': 'Korean', 'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi',
            'th': 'Thai', 'vi': 'Vietnamese', 'tr': 'Turkish', 'pl': 'Polish',
            'nl': 'Dutch', 'sv': 'Swedish', 'no': 'Norwegian', 'fi': 'Finnish',
            'el': 'Greek'
        }
    
    def translate_analysis_results(self, results: Dict[str, Any], target_lang: str = 'en') -> Dict[str, Any]:
        if target_lang == results.get('extracted_data', {}).get('language', 'en'):
            return results
        
        translated = results.copy()
        
        # Translate job matches
        if 'job_matches' in translated:
            for job in translated['job_matches']:
                job['match_reasons'] = self._translate_list(job.get('match_reasons', []), target_lang)
        
        # Translate suggestions
        if 'suggestions' in translated:
            translated['suggestions'] = self._translate_list(translated['suggestions'], target_lang)
        
        # Translate analysis
        if 'analysis' in translated:
            analysis = translated['analysis']
            if 'suggestions' in analysis:
                analysis['suggestions'] = self._translate_list(analysis['suggestions'], target_lang)
            if 'strengths' in analysis:
                analysis['strengths'] = self._translate_list(analysis['strengths'], target_lang)
            if 'weaknesses' in analysis:
                analysis['weaknesses'] = self._translate_list(analysis['weaknesses'], target_lang)
        
        return translated
    
    def _translate_list(self, items: List[str], target_lang: str) -> List[str]:
        try:
            # Validate target language
            if target_lang not in self.supported_languages:
                return items
            
            translated_items = []
            for item in items[:10]:  # Limit to 10 items
                if item and len(item.strip()) > 0 and len(item) < 500:
                    # Sanitize input
                    clean_item = html.escape(item.strip())
                    result = self.translator.translate(clean_item, dest=target_lang)
                    translated_items.append(html.unescape(result.text))
                    time.sleep(0.1)  # Rate limiting
                else:
                    translated_items.append(item)
            return translated_items
        except Exception:
            return items  # Return original if translation fails