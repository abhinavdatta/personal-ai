import torch
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wavfile
from engine.qa_engine import answer

# Detect device automatically
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load Whisper model
print(f"🎙 Loading Whisper on {DEVICE}...")
model = whisper.load_model("small", device=DEVICE)


def find_best_input_device():
    devices = sd.query_devices()

    # First: prefer WASAPI microphones (best for Windows)
    for i, dev in enumerate(devices):
        name = dev["name"].lower()
        if dev["max_input_channels"] > 0 and "wasapi" in name:
            return i

    # Fallback: any input device
    for i, dev in enumerate(devices):
        if dev["max_input_channels"] > 0:
            return i

    return None


def record_audio(duration=5, samplerate=16000):
    print("🎤 Listening...")

    input_device = find_best_input_device()
    if input_device is None:
        raise RuntimeError("No microphone found")

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32",
        device=input_device
    )
    sd.wait()
    return audio, samplerate


def transcribe_audio():
    audio, samplerate = record_audio()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wavfile.write(f.name, samplerate, audio)
        result = model.transcribe(f.name)

    text = result["text"].strip()
    print(f"🗣 You said: {text}")
    return text


def listen_and_answer():
    try:
        question = transcribe_audio()
        if question:
            response = answer(question)
            print("🤖", response)
    except Exception as e:
        print("Voice error:", e)
