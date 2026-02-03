import hashlib
import time
from dataclasses import dataclass
from getpass import getpass
from typing import Optional


@dataclass
class AuthResult:
    success: bool
    message: str


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class SecurityManager:
    def __init__(self, password_hash: str, voice_passphrase: str, timeout_seconds: int) -> None:
        self._password_hash = password_hash
        self._voice_passphrase = voice_passphrase
        self._timeout_seconds = timeout_seconds
        self._unlocked_at: Optional[float] = None

    @property
    def is_locked(self) -> bool:
        if self._unlocked_at is None:
            return True
        if time.time() - self._unlocked_at > self._timeout_seconds:
            self.lock()
            return True
        return False

    def lock(self) -> None:
        self._unlocked_at = None

    def _unlock(self) -> None:
        self._unlocked_at = time.time()

    def authenticate_password(self) -> AuthResult:
        if not self._password_hash:
            return AuthResult(False, "Password hash not configured.")
        password = getpass("Enter ERROR password: ")
        if hash_password(password) == self._password_hash:
            self._unlock()
            return AuthResult(True, "Authentication successful.")
        return AuthResult(False, "Invalid password.")

    def authenticate_voice(self, phrase: str) -> AuthResult:
        if not self._voice_passphrase:
            return AuthResult(False, "Voice passphrase not configured.")
        if phrase.strip().lower() == self._voice_passphrase.strip().lower():
            self._unlock()
            return AuthResult(True, "Voice authentication successful.")
        return AuthResult(False, "Voice authentication failed.")

    def refresh_session(self) -> None:
        if not self.is_locked:
            self._unlocked_at = time.time()
