from error_assistant.assistant import ErrorAssistant
from error_assistant.config import Settings
from error_assistant.logger import setup_logging


def main() -> None:
    settings = Settings()
    setup_logging(settings.log_level)
    assistant = ErrorAssistant(settings)
    assistant.run()


if __name__ == "__main__":
    main()
