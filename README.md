# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational AI web application based on the project specification.

## Features

- Ask questions and receive AI-generated answers
- Explain difficult concepts in simple language
- Generate multiple-choice quizzes
- Summarize educational passages
- Generate personalized learning paths
- Optional Google Search grounding for current/time-sensitive questions
- FastAPI backend
- HTML/CSS/JavaScript frontend
- Environment-based API-key configuration
- Structured quiz output validation

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## 1. Install Python

Use Python 3.10 or newer.

Check:

```bash
python --version
```

## 2. Open the project in VS Code

Open the `EduGenie` folder.

## 3. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Create the API key file

Copy:

```text
.env.example
```

to:

```text
.env
```

Then put your Gemini API key in:

```env
GEMINI_API_KEY=YOUR_REAL_KEY
```

Do not upload `.env` to GitHub.

The default model is:

```env
GEMINI_MODEL=gemini-3.8-flash
```

You can change it later if your Google AI Studio account provides access to another compatible Gemini model.

## 6. Run EduGenie

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 7. Test

### Health check

Open:

```text
http://127.0.0.1:8000/health
```

You should see JSON similar to:

```json
{
  "status": "ok",
  "model": "gemini-3.8-flash"
}
```

### Question test

Try:

```text
What is inheritance in Java?
```

### Current-fact test

Enable:

```text
Use web grounding for current facts
```

Then ask something time-sensitive, such as:

```text
What is the latest version of Python?
```

### Quiz test

Enter:

```text
Pythagoras theorem
```

### Summary test

Paste a paragraph and click Summarize.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web interface |
| GET | `/health` | Server/model health |
| POST | `/api/qa` | Question answering |
| POST | `/api/explain` | Concept explanation |
| POST | `/api/quiz` | Quiz generation |
| POST | `/api/summarize` | Summarization |
| POST | `/api/learn/recommendations` | Learning path |

## Important accuracy design

EduGenie does not claim that AI answers are automatically perfect.

The application uses:
- strong educational system prompts
- low temperature for more consistent responses
- structured validation for quiz generation
- explicit anti-hallucination instructions
- optional Google Search grounding for current facts

For high-stakes subjects, users should verify important information against authoritative sources.

## Troubleshooting

### `GEMINI_API_KEY is missing`

Make sure:
1. `.env` exists in the project root.
2. It contains `GEMINI_API_KEY=...`.
3. You restarted the server after changing `.env`.

### `ModuleNotFoundError`

Activate the virtual environment and run:

```bash
pip install -r requirements.txt
```

### Gemini model access error

Change `GEMINI_MODEL` in `.env` to a Gemini model available to your API project.

### Port already in use

Run:

```bash
uvicorn main:app --reload --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```
