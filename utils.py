import re
from typing import Optional, Tuple
from pathlib import Path

def detect_language(prompt: str) -> Tuple[str, str]:
    """Detect language from prompt command and return (language, cleaned_prompt)."""
    language_map = {
        '!bash': 'bash',
        '!python': 'python',
        '!js': 'javascript',
        '!json': 'json',
        '!yaml': 'yaml',
        '!html': 'html',
        '!css': 'css'
    }
    
    for cmd, lang in language_map.items():
        if prompt.startswith(cmd):
            return lang, prompt[len(cmd):].strip()
    
    return None, prompt

def extract_code_blocks(text: str) -> list:
    """Extract all code blocks from markdown text."""
    pattern = r'```(?:[a-zA-Z0-9]+)?\n([\s\S]*?)\n```'
    return re.findall(pattern, text)

def get_file_content(file_path: str) -> Optional[str]:
    """Read file content if it exists."""
    path = Path(file_path)
    if path.exists() and path.is_file():
        return path.read_text()
    return None