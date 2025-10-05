import re
import html
from typing import Any, Dict, List

class SecurityValidator:
    @staticmethod
    def sanitize_string(text: str, max_length: int = 1000) -> str:
        if not text:
            return ""
        # Remove HTML tags and escape special characters
        text = re.sub(r'<[^>]+>', '', str(text))
        text = html.escape(text)
        return text[:max_length]
    
    @staticmethod
    def validate_filename(filename: str) -> bool:
        if not filename or len(filename) > 255:
            return False
        # Check for path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return False
        return True
    
    @staticmethod
    def validate_file_size(size: int, max_size: int = 10 * 1024 * 1024) -> bool:
        return 0 < size <= max_size
    
    @staticmethod
    def validate_language_code(code: str) -> bool:
        return bool(code and len(code) == 2 and code.isalpha())
    
    @staticmethod
    def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized[key] = SecurityValidator.sanitize_string(value)
            elif isinstance(value, list):
                sanitized[key] = [SecurityValidator.sanitize_string(str(item)) for item in value[:20]]
            else:
                sanitized[key] = value
        return sanitized