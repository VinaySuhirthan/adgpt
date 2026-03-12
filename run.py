from dotenv import load_dotenv
import os

load_dotenv()

brain = os.getenv('BRAIN', 'True').lower() == 'true'  # True = Qwen / Ollama (app.py) | False = Groq (appbc:app)
allow_groq_fallback = os.getenv('ALLOW_GROQ_FALLBACK', 'False').lower() == 'true'  # False = strictly Ollama, no fallback | True = allow fallback to Groq

import subprocess
import sys

# Get port from environment variables (Render/Heroku compatible) or default to 8000
port = os.getenv("PORT", "8000")

module = "question_mode.app:app" if brain else "question_mode.appbc:app"
label = "Qwen / Ollama (via question_mode)" if brain else "Groq (via question_mode)"

print(f"[switch] Brain: {label}")
print(f"[switch] Module: {module}")
print(f"[switch] Groq Fallback: {'ENABLED' if allow_groq_fallback else 'DISABLED'}")
print(f"[switch] Starting server on http://0.0.0.0:{port}")

# Set environment variable for app.py to use
env = os.environ.copy()
env["GROQ_FALLBACK_ENABLED"] = "true" if allow_groq_fallback else "false"

proc = subprocess.Popen([
    sys.executable, "-m", "uvicorn", module,
    "--reload",
    "--host", "0.0.0.0",
    "--port", port,
], env=env)

try:
    proc.wait()
except KeyboardInterrupt:
    print("[switch] Shutting down server...")
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()