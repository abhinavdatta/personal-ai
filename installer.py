import os
import subprocess
import shutil
import sys


def run(cmd):
    subprocess.run(cmd, shell=True)


def install_python_packages():
    print("Installing Python dependencies...")
    run("pip install -r requirements.txt")


def install_ffmpeg():
    if shutil.which("ffmpeg"):
        print("FFmpeg already installed.")
        return

    print("Installing FFmpeg...")
    run(
        'powershell -Command "Invoke-WebRequest '
        'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip '
        '-OutFile ffmpeg.zip"'
    )
    run('powershell -Command "Expand-Archive ffmpeg.zip -DestinationPath C:\\ffmpeg"')

    # Add to PATH
    os.system(
        'setx PATH "%PATH%;C:\\ffmpeg\\ffmpeg-*-essentials_build\\bin"'
    )


def install_ollama():
    if shutil.which("ollama"):
        print("Ollama already installed.")
        return

    print("Installing Ollama...")
    run(
        'powershell -Command "Invoke-WebRequest '
        'https://ollama.com/download/OllamaSetup.exe '
        '-OutFile OllamaSetup.exe"'
    )
    run("OllamaSetup.exe")


def main():
    print("=== StudyAI Installer ===")

    install_python_packages()
    install_ffmpeg()
    install_ollama()

    print("Installation complete.")
    print("Launching StudyAI...")

    run("main.exe")


if __name__ == "__main__":
    main()
