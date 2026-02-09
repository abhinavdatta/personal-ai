# StudyAI Assistant

StudyAI Assistant is a **local AI-powered study helper** that can read your PDFs, understand images, accept voice questions, and answer using local AI models like **Mistral, DeepSeek, or GPT-OSS** via Ollama.

It runs **fully offline** (except optional web searches) and can be packaged into a single `.exe` installer.

---

## Features

* Local AI models via **Ollama**
* Train on **PDF study materials**
* Image understanding (diagrams, circuits, etc.) "need to be fixed"
* OCR for scanned PDFs "works but dont know how to add"
* Voice input using **Whisper** "Works but when used on app it crashes"
* GUI interface
* Background retraining
* Auto-installer for dependencies "Broken needs to be fixed"
* CPU/GPU auto-detection " planning to add this feature"
* optimization "I still need to figure how optimization works because this takes so much resources"

---
<img width="527" height="779" alt="image" src="https://github.com/user-attachments/assets/e9af3be4-f40a-4316-a64f-8ed8a6d196a0" />


## Requirements

* Windows 10/11
* Python **3.11** (recommended)
* Ollama must be installed

Download Ollama:
[https://ollama.com](https://ollama.com)

---

## Installation (Developer Mode)

Open terminal inside the project folder:

### 1. Create virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the app

```powershell
python main.py
```

---

## Training the AI with PDFs

Place study material inside:

```
data/pdfs/
```

Then run:

```powershell
python -c "from engine.pdf_ingest import ingest_pdfs; ingest_pdfs()"
```

This builds the AI memory.

---

## Building the Installer (.exe)

Install PyInstaller:

```powershell
pip install pyinstaller
```

Then build:

```powershell
pyinstaller --onefile installer.py
```

Output:

```
dist/installer.exe
```

This `.exe` will:

* Install dependencies
* Start Ollama
* Launch the AI assistant

---

## Supported AI Models

You can use any installed Ollama model:

Examples:

```powershell
ollama pull mistral
ollama pull deepseek-r1
ollama pull gpt-oss:20b
```

The model can be selected from the GUI.

---

## Voice Commands

Press the **Voice** button and speak your question.
Whisper will transcribe it and the AI will answer.

---

## GPU Support

The app automatically:

* Uses **GPU** if available
* Falls back to **CPU** if not

No configuration needed.

---

## Notes

* First run may take time due to model loading.
* Whisper downloads its model automatically.
* Ollama must be installed on the system.

---

## Future Improvements

* ChatGPT-style interface
* Automatic model download
* Installer wizard

---

## License
This is a personal educational project. Feel free to use it however you like. If you’re able to fix most of the bugs, thank you!

