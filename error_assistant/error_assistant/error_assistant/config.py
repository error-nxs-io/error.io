from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    name: str = "ERROR"
    api_base_url: str = os.getenv("ERROR_API_BASE_URL", "")
    api_key: str = os.getenv("ERROR_API_KEY", "")
    data_dir: Path = Path(os.getenv("ERROR_DATA_DIR", "data"))
    preferences_file: str = "preferences.json"
    context_file: str = "context.json"
    log_level: str = os.getenv("ERROR_LOG_LEVEL", "INFO")
    session_timeout_seconds: int = int(os.getenv("ERROR_SESSION_TIMEOUT", "300"))
    password_hash: str = os.getenv("ERROR_PASSWORD_HASH", "")
    voice_passphrase: str = os.getenv("ERROR_VOICE_PASSPHRASE", "")

    @property
    def preferences_path(self) -> Path:
        return self.data_dir / self.preferences_file

    @property
    def context_path(self) -> Path:
        return self.data_dir / self.context_file
