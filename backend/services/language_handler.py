from typing import Dict, Any
from langdetect import detect

class LanguageHandler:
    def __init__(self):
        self.language_names = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'ko': 'Korean', 'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi',
            'th': 'Thai', 'vi': 'Vietnamese', 'tr': 'Turkish', 'pl': 'Polish',
            'nl': 'Dutch', 'sv': 'Swedish', 'no': 'Norwegian', 'fi': 'Finnish',
            'el': 'Greek'
        }
    
    def detect_language(self, text: str) -> str:
        try:
            return detect(text)
        except:
            return 'en'
    
    def get_language_name(self, code: str) -> str:
        return self.language_names.get(code, code.upper())
    
    def should_translate(self, detected_lang: str, target_lang: str = 'en') -> bool:
        return detected_lang != target_lang and detected_lang in self.language_names