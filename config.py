import os
from pathlib import Path
from dotenv import load_dotenv
import yaml

load_dotenv()

class Config:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("MODEL", "anthropic/claude-3-haiku")
        self.config_path = Path.home() / ".config" / "devos-ai"
        self.config_file = self.config_path / "config.yaml"
        
        # Create config directory if it doesn't exist
        self.config_path.mkdir(parents=True, exist_ok=True)
        
        # Load or create config file
        if not self.config_file.exists():
            self._create_default_config()
        self._load_config()
    
    def _create_default_config(self):
        default_config = {
            "model": self.model,
            "theme": "monokai",
            "max_tokens": 2000,
            "temperature": 0.7
        }
        with open(self.config_file, 'w') as f:
            yaml.safe_dump(default_config, f)
    
    def _load_config(self):
        with open(self.config_file, 'r') as f:
            self.config = yaml.safe_load(f) or {}
        
        # Update instance attributes from config
        self.model = self.config.get("model", self.model)
        self.theme = self.config.get("theme", "monokai")
        self.max_tokens = self.config.get("max_tokens", 2000)
        self.temperature = self.config.get("temperature", 0.7)
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            yaml.safe_dump({
                "model": self.model,
                "theme": self.theme,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }, f)

# Instantiate the configuration
config = Config()
