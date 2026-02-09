import os
import hashlib
import json
import threading
import time

from engine.pdf_ingest import ingest_pdfs

STATE_FILE = "embeddings/retrain_state.json"
PDF_DIR = "data/pdfs"
CHECK_INTERVAL = 120  # seconds (2 minutes)

def file_hash(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def scan_pdfs():
    state = load_state()
    changed = False

    for file in os.listdir(PDF_DIR):
        if not file.endswith(".pdf"):
            continue

        path = os.path.join(PDF_DIR, file)
        h = file_hash(path)

        if file not in state or state[file] != h:
            state[file] = h
            changed = True

    if changed:
        print("🔁 PDF changes detected → retraining")
        ingest_pdfs()
        save_state(state)

def start_background_retraining():
    def loop():
        while True:
            try:
                scan_pdfs()
            except Exception:
                pass
            time.sleep(CHECK_INTERVAL)

    threading.Thread(target=loop, daemon=True).start()
