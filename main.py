import subprocess
import shutil
import time
import sys
import threading

from ui.overlay import Overlay
from ui.hotkeys import bind_hotkeys
from ui.tray import run_tray
from engine.retrain_manager import start_background_retraining


# ---------------------------
# Ollama management
# ---------------------------
def ollama_installed():
    return shutil.which("ollama") is not None


def ollama_running():
    try:
        subprocess.check_output(["ollama", "list"])
        return True
    except Exception:
        return False


def start_ollama():
    subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )


def ensure_ollama():
    if not ollama_installed():
        print("Ollama not installed. Install from https://ollama.com")
        sys.exit(1)

    if not ollama_running():
        start_ollama()
        time.sleep(2)


# ---------------------------
# App start
# ---------------------------
def main():
    # Ensure Ollama is ready
    ensure_ollama()

    # Start background retraining
    start_background_retraining()

    # Start tray icon
    threading.Thread(target=run_tray, daemon=True).start()
    overlay = Overlay() 
    bind_hotkeys(overlay)

# Show overlay at startup
    overlay.show("StudyAI ready")

    overlay.root.mainloop()


if __name__ == "__main__":
    main()
