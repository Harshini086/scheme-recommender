# SchemeSetu — Government Scheme Recommender

Find government schemes you may be eligible for, based on a citizen profile.
**College/prototype project.** All scheme data is synthetic demonstration data —
verify with official government sources before applying. Results are **not**
an official eligibility determination.

## Features
- Multi-step profile form
- Rule-based recommendation engine (no LLM required) with transparent match %
- Scheme details with matched/failed criteria explanation
- Document readiness dashboard
- Search & filter across 39 synthetic schemes
- Scheme Assistant chatbot (works fully offline; optional LLM upgrade)
- Demo profile button for quick presentation

## Project Structure
```
app.py                  Entry point — home + profile form
engine/                 Recommendation engine (eligibility, scoring, orchestration)
pages/                  Streamlit multi-page UI (dashboard, browse, details, docs, chatbot)
utils/                  Data loading + shared helpers
data/schemes.json       Synthetic scheme dataset
```

## Local Setup (Windows / PowerShell)
```powershell
python --version
python -m venv venv
.\venv\Scripts\Activate.ps1
```
If activation is blocked, run once:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Install dependencies:
```powershell
pip install -r requirements.txt
```
Run:
```powershell
streamlit run app.py
```
Open the URL shown (usually http://localhost:8501).

## Optional: Enable LLM Chatbot
Copy `.env.example` to `.env` and add an API key, or set it as an environment
variable before running. Without a key, the chatbot uses its built-in local
fallback (keyword search over the scheme dataset) — the app never crashes due
to a missing key.

## Swapping in Real Data Later
Replace `data/schemes.json` with data from a database or government API —
just keep the same field names. `utils/data_loader.py` and `engine/` never
need to change.

## Disclaimer
This application provides informational recommendations based on the
information entered by the user. Eligibility shown here is not an official
government determination. Scheme details and eligibility requirements should
be verified with the relevant official government source before applying.
