# AI Tic-Tac-Toe — Setup & Installation

## Prerequisites

Make sure the following are installed before proceeding:

- **Python 3.8+** — [python.org/downloads](https://www.python.org/downloads/)
- **pip** — included with Python 3.4+
- A modern web browser (Chrome, Firefox, Edge, etc.)

---

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/AIFinalProj.git
cd AIFinalProj
```

---

## 2. Backend Setup

Navigate into the backend directory and install the required Python packages.

```bash
cd backend
pip install flask flask-cors
```

### Start the Flask Server

```bash
python app.py
```

The backend will start on **http://127.0.0.1:5000**. You should see output similar to:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

> **Note:** Keep this terminal window open while playing. The frontend depends on it.

---

## 3. Frontend Setup

No build step or package manager is required. Open a **new terminal tab**, navigate to the frontend directory, and open `index.html` directly in your browser.

### Option A — Open directly

```bash
cd frontend
open index.html        # macOS
start index.html       # Windows
xdg-open index.html    # Linux
```

### Option B — Serve with Python (recommended to avoid CORS issues)

```bash
cd frontend
python -m http.server 8080
```

Then visit **http://localhost:8080** in your browser.

---

## 4. Verify Connection

Once both the backend and frontend are running, the status indicator in the UI should display:

```
Backend connected on port 5000
```

If it shows an error, confirm the Flask server is running and accessible at `http://127.0.0.1:5000/health`.

---

## Project Structure

```
AIFinalProj/
├── backend/
│   ├── app.py          # Flask API server
│   ├── minimax.py      # Minimax algorithm + Alpha-Beta pruning
│   ├── game.py         # Board logic, win/draw detection
│   └── analytics.py    # Move analysis and metrics
└── frontend/
    ├── index.html      # Main UI
    ├── app.js          # Game logic and API calls
    └── easy.jpg        # Difficulty assets
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: flask` | Run `pip install flask flask-cors` |
| "Backend not running on port 5000" | Ensure `python app.py` is running in the backend directory |
| CORS errors in browser console | Use Option B (Python HTTP server) instead of opening the HTML file directly |
| Port 5000 already in use | Run `python app.py` after killing the existing process using that port |
