import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
import sys

# Global states
voice_enabled = True
overlay_enabled = True


def create_icon_image():
    # Create a simple square icon
    img = Image.new("RGB", (64, 64), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    draw.rectangle((16, 16, 48, 48), fill=(0, 200, 255))
    return img


def toggle_voice(icon, item):
    global voice_enabled
    voice_enabled = not voice_enabled
    print(f"Voice enabled: {voice_enabled}")


def toggle_overlay(icon, item):
    global overlay_enabled
    overlay_enabled = not overlay_enabled
    print(f"Overlay enabled: {overlay_enabled}")


def quit_app(icon, item):
    print("Exiting...")
    icon.stop()
    sys.exit(0)


def run_tray():
    icon = pystray.Icon("StudyAI")

    icon.icon = create_icon_image()
    icon.menu = pystray.Menu(
        item("Toggle Voice", toggle_voice),
        item("Toggle Overlay", toggle_overlay),
        item("Exit", quit_app)
    )

    icon.run()
