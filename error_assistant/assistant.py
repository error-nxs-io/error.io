import logging
from typing import Any, Dict

from .api_client import APIClient
from .command_processing import CommandProcessor
from .config import Settings
from .security import SecurityManager
from .storage import load_json, save_json
from .system_control import SystemController
from .voice_recognition import VoiceRecognizer


class ErrorAssistant:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._logger = logging.getLogger(settings.name)
        self._voice = VoiceRecognizer()
        self._api_client = APIClient(settings.api_base_url, settings.api_key)
        self._processor = CommandProcessor(self._api_client)
        self._controller = SystemController()
        self._security = SecurityManager(
            settings.password_hash,
            settings.voice_passphrase,
            settings.session_timeout_seconds,
        )
        self._preferences: Dict[str, Any] = load_json(
            settings.preferences_path,
            {"name": settings.name, "preferences": {}},
        )
        self._context: Dict[str, Any] = load_json(settings.context_path, {"history": []})

    def run(self) -> None:
        self._logger.info("%s assistant initialized and locked.", self._settings.name)
        while True:
            utterance = self._voice.listen()
            if utterance is None:
                self._logger.info("Shutting down assistant.")
                break
            if not utterance:
                continue
            if utterance.lower() in {"exit", "quit"}:
                self._logger.info("Exit command received.")
                break
            if self._security.is_locked:
                self._handle_locked_state(utterance)
                continue
            self._security.refresh_session()
            command = self._processor.interpret(utterance, self._context)
            if command.intent == "lock":
                self._security.lock()
                self._respond("Session locked.")
                continue
            success, message = self._controller.dispatch(command.intent, command.parameters)
            reply = command.response or message
            self._respond(reply)
            self._update_context(utterance, reply, success)

    def _handle_locked_state(self, utterance: str) -> None:
        if utterance.lower().startswith("password "):
            result = self._security.authenticate_password()
            self._respond(result.message)
            return
        if utterance.lower().startswith("voice "):
            phrase = utterance[6:]
            result = self._security.authenticate_voice(phrase)
            self._respond(result.message)
            return
        self._respond("Session is locked. Say 'password' or 'voice' to authenticate.")

    def _respond(self, text: str) -> None:
        self._logger.info("%s", text)
        print(f"{self._settings.name}: {text}")

    def _update_context(self, user_text: str, reply: str, success: bool) -> None:
        self._context["history"].append(
            {"user": user_text, "assistant": reply, "success": success}
        )
        if len(self._context["history"]) > 50:
            self._context["history"] = self._context["history"][-50:]
        save_json(self._settings.context_path, self._context)
        save_json(self._settings.preferences_path, self._preferences)
