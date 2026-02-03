import os
import platform
import shutil
import subprocess
import webbrowser
from pathlib import Path
from typing import Any, Dict, Tuple


class SystemController:
    def __init__(self) -> None:
        self._platform = platform.system().lower()

    def dispatch(self, intent: str, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        handler = getattr(self, f"handle_{intent}", None)
        if not handler:
            return False, f"No handler for intent '{intent}'."
        return handler(parameters)

    def handle_open_app(self, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        name = parameters.get("name", "")
        if not name:
            return False, "Application name missing."
        try:
            if self._platform == "windows":
                os.startfile(name)
            elif self._platform == "darwin":
                subprocess.Popen(["open", "-a", name])
            else:
                subprocess.Popen([name])
        except Exception as exc:
            return False, f"Failed to open app: {exc}"
        return True, f"Opening {name}."

    def handle_close_app(self, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        name = parameters.get("name", "")
        if not name:
            return False, "Application name missing."
        try:
            if self._platform == "windows":
                subprocess.run(["taskkill", "/IM", name, "/F"], check=False)
            else:
                subprocess.run(["pkill", "-f", name], check=False)
        except Exception as exc:
            return False, f"Failed to close app: {exc}"
        return True, f"Closing {name}."

    def handle_browse(self, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        url = parameters.get("url", "")
        if not url:
            return False, "URL missing."
        webbrowser.open(url)
        return True, f"Opening {url}."

    def handle_create_file(self, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        path = parameters.get("path", "")
        if not path:
            return False, "File path missing."
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
        return True, f"Created file at {file_path}."

    def handle_delete_file(self, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        path = parameters.get("path", "")
        if not path:
            return False, "File path missing."
        file_path = Path(path)
        if not file_path.exists():
            return False, "File not found."
        file_path.unlink()
        return True, f"Deleted file at {file_path}."

    def handle_move_file(self, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        source = parameters.get("source", "")
        destination = parameters.get("destination", "")
        if not source or not destination:
            return False, "Source or destination missing."
        shutil.move(source, destination)
        return True, f"Moved {source} to {destination}."

    def handle_copy_file(self, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        source = parameters.get("source", "")
        destination = parameters.get("destination", "")
        if not source or not destination:
            return False, "Source or destination missing."
        shutil.copy2(source, destination)
        return True, f"Copied {source} to {destination}."

    def handle_search_files(self, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        query = parameters.get("query", "")
        if not query:
            return False, "Search query missing."
        matches = []
        for root, _, files in os.walk(Path.home()):
            for filename in files:
                if query.lower() in filename.lower():
                    matches.append(str(Path(root) / filename))
                    if len(matches) >= 10:
                        break
            if len(matches) >= 10:
                break
        if not matches:
            return True, "No files found."
        return True, "Found files:\n" + "\n".join(matches)

    def handle_shutdown(self, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        if self._platform == "windows":
            cmd = ["shutdown", "/s", "/t", "0"]
        elif self._platform == "darwin":
            cmd = ["sudo", "shutdown", "-h", "now"]
        else:
            cmd = ["shutdown", "now"]
        return False, f"Shutdown command prepared: {' '.join(cmd)}"

    def handle_restart(self, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        if self._platform == "windows":
            cmd = ["shutdown", "/r", "/t", "0"]
        elif self._platform == "darwin":
            cmd = ["sudo", "shutdown", "-r", "now"]
        else:
            cmd = ["shutdown", "-r", "now"]
        return False, f"Restart command prepared: {' '.join(cmd)}"

    def handle_lock(self, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        return True, "Locking session."

    def handle_unknown(self, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        text = parameters.get("text", "")
        return False, f"I didn't understand: {text}"
