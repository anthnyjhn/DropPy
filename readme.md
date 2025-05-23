# DropPy – local file-sharing app

**DropPy** is a lightweight Python app that lets you receive files over your local network. Simply run the server and scan the QR code to start uploading from any device on the same Wi-Fi.

---

## Setup Instructions

### 1. Navigate to the Project Directory

Ensure you're in the same directory where `DropPy.py` is located:

```bash
cd /path/to/DropPy/
```

### 2. Install Python Virtual Environment (if not already installed)

for Linux:

```bash
sudo apt install python3-venv -y
```

### 3. Create a Virtual Environment for DropPy

For Linux/macOS/Windows:
In your terminal, run:

```bash
python3 -m venv venv
```

### 4. Activate the Environment

For Linux/macOS:
In your terminal, run:

```bash
source venv/bin/activate
```

For Windows:
In Command Prompt or PowerShell, run:

```cmd
venv/bin/activate
```

### 5. Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

## Running DropPy

For Linux/macOS/Windows:
In your terminal, run:

```bash
python3 DropPy.py
```

---

## Uploaded Files

By default, files will be saved in ~/MyDropbox. You can specify a different folder the first time you run the app.
