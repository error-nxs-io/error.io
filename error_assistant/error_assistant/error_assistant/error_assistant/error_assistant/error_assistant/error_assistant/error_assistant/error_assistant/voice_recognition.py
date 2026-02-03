from typing import Optional


class VoiceRecognizer:
    def __init__(self) -> None:
        self._active = True

    def stop(self) -> None:
        self._active = False

    def listen(self) -> Optional[str]:
        if not self._active:
            return None
        try:
            return input("You: ").strip()
        except EOFError:
            return None
