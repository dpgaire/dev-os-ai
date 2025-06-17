import os
import subprocess
from pathlib import Path
from typing import List, Optional
import tempfile

class FileHandler:
    @staticmethod
    def read_file(file_path: str) -> Optional[str]:
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @staticmethod
    def write_file(file_path: str, content: str) -> str:
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            return f"File {file_path} written successfully"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    @staticmethod
    def find_files(pattern: str, directory: str = ".") -> List[str]:
        try:
            return list(map(str, Path(directory).rglob(pattern)))
        except Exception as e:
            return [f"Error finding files: {str(e)}"]

    @staticmethod
    def create_temp_file(content: str, suffix: str = ".txt") -> str:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(content.encode())
            return tmp.name