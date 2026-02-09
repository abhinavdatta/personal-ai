import keyboard
import threading
from ui.voice import listen_and_answer


def bind_hotkeys(overlay):
    # Toggle overlay visibility
    keyboard.add_hotkey("ctrl+shift+o", overlay.toggle)

    # Voice trigger
    keyboard.add_hotkey(
        "ctrl+shift+v",
        lambda: threading.Thread(target=listen_and_answer, daemon=True).start()
    )

    print("Hotkeys:")
    print("CTRL + SHIFT + O → Toggle overlay")
    print("CTRL + SHIFT + V → Voice question")
