-# error.io
-error.io is an intelligent assistant that helps developers understand and fix coding errors using AI APIs. It supports multiple languages, frameworks, and provides real-time solutions.
+# ERROR Assistant
+
+ERROR is a secure, voice-first personal operating assistant that connects to your existing API for natural language understanding. It runs locally, stays locked by default, and only controls your machine after successful authentication.
+
+## Features
+
+- **Voice control & command processing** (console-based placeholder for mic input)
+- **Full PC management**: open/close apps, file operations, browsing, and system actions
+- **Security layer**: locked by default, password/voice auth, session timeout
+- **AI intelligence**: integrates with your API for intent detection and context
+- **Modular architecture**: dedicated modules for voice, commands, system control, API, and security
+
+## Quick Start
+
+```bash
+python main.py
+```
+
+Type commands in the console (replace with microphone input when integrating a speech engine).
+
+## Authentication
+
+Set environment variables before launching:
+
+```bash
+export ERROR_PASSWORD_HASH="$(python -c 'import hashlib; print(hashlib.sha256(b"your-password").hexdigest())')"
+export ERROR_VOICE_PASSPHRASE="your voice passphrase"
+```
+
+ERROR starts in a locked state. Use:
+
+- `password` to trigger password authentication
+- `voice <phrase>` to authenticate with a passphrase
+
+## API Configuration
+
+Set your API endpoint and key:
+
+```bash
+export ERROR_API_BASE_URL="https://your-api"
+export ERROR_API_KEY="your-key"
+```
+
+Expected API response from `POST /interpret`:
+
+```json
+{
+  "intent": "open_app",
+  "parameters": {"name": "Calculator"},
+  "reply": "Opening Calculator."
+}
+```
+
+If the API is unreachable, ERROR falls back to a rule-based intent parser.
+
+## Project Structure
+
+```
+error_assistant/
+  assistant.py
+  api_client.py
+  command_processing.py
+  config.py
+  logger.py
+  security.py
+  storage.py
+  system_control.py
+  voice_recognition.py
+main.py
+```
+
+## Notes
+
+System control for shutdown/restart is intentionally returned as a prepared command for safety. Update `SystemController` for your environment before enabling destructive actions.
 
EOF
)
