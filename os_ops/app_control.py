import subprocess
import platform
import psutil
from typing import List, Optional

class AppController:
    @staticmethod
    def open_app(app_name: str) -> str:
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                subprocess.run(["open", "-a", app_name], check=True)
            elif system == "Windows":
                subprocess.run(["start", app_name], shell=True, check=True)
            else:  # Linux
                subprocess.run([app_name], check=True)
            return f"Opened {app_name}"
        except Exception as e:
            return f"Error opening app: {str(e)}"

    @staticmethod
    def list_running_apps() -> List[str]:
        """Get list of running applications with details"""
        try:
            apps = []
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    apps.append(f"{proc.info['name']} (PID: {proc.info['pid']}, User: {proc.info['username']})")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return apps
        except Exception as e:
            return [f"Error listing apps: {str(e)}"]

    @staticmethod
    def kill_app(app_name: str) -> str:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == app_name:
                proc.kill()
                return f"Terminated {app_name}"
        return f"App {app_name} not found"