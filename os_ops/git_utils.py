import subprocess
from pathlib import Path
from typing import Dict, Optional

class GitManager:
    @staticmethod
    def get_status(repo_path: str = ".") -> Dict[str, str]:
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True
            )
            return {
                "status": result.stdout.strip(),
                "branch": GitManager._get_current_branch(repo_path)
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def _get_current_branch(repo_path: str) -> Optional[str]:
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except:
            return None