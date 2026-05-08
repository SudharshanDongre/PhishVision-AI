# PhishVision

PhishVision is a lightweight Streamlit-based web app for phishing detection and analysis. It provides a compact UI to scan URLs, run bulk scans, inspect threat intelligence, and select machine-learning detection engines. The project includes a browser extension helper, model training and inference utilities, and a simple API layer for programmatic access.

This README describes how to set up, run, and contribute to the project locally.

--

## Features

- URL scanning and rule-based feature extraction
- Multiple ML detection engines (Gradient Boosting, XGBoost, Random Forest, Stacking/Ensemble)
- Bulk scan support and CSV import/export
- Browser extension for quick scans from the browser
- Admin/auth utilities and a small API for inference
- Custom themed Streamlit UI with an expandable sidebar and model selector

## Repository structure

- `app.py` — Main Streamlit application and frontend styling
- `api.py` — Minimal API endpoints for model inference and integration
- `auth.py`, `auth_ui.py` — Authentication helpers and UI
- `train.py` — Training script for ML models
- `model.py` — Model loading and inference helpers
- `extractor.py` — Feature extraction and rule-based checks
- `news_component.py` — UI component for threat news/notifications
- `browser-extension/` — Chrome extension source (popup + content script)
- `requirements.txt` — Python package dependencies
- `Phishing.csv`, `test.csv` — Example data files

## Prerequisites

- Python 3.10+ (virtualenv / venv recommended)
- Git (to clone the repo)

On Windows, using the included `myenv` virtual environment is possible, but creating a fresh venv is recommended to avoid environment-specific issues.

## Quick start (local)

1. Clone the repository

```bash
git clone <repo-url> PhishVision
cd PhishVision
```

2. Create and activate a virtual environment (recommended)

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the Streamlit app

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501` by default.

## Configuration

- Environment variables (optional): The app may use a `.env` file for secrets and API keys. Create a `.env` at the repo root when needed.
- `initial_sidebar_state` and theming are configured in `app.py`.

## Models & Training

- Training logic is implemented in `train.py`. Models are saved/loaded via `joblib` in `model.py`.
- Example datasets (`Phishing.csv`, `test.csv`) are included for experimentation.
- The UI provides a model selection dropdown (Detection Engine) which chooses the inference model used by `api.py`.

## Browser extension

The `browser-extension/` folder contains a simple Chrome extension that can send URLs to the PhishVision UI for quick scanning. To load it in Chrome/Edge:

1. Open `chrome://extensions` and enable Developer mode.
2. Click "Load unpacked" and select the `browser-extension` folder.

## Testing & Debugging

- Use `test.py` for quick sanity checks and `verify_data.py` to validate input CSVs.
- Inspect logs in the terminal where Streamlit is running.

## Development notes

- UI styling is centralized in `app.py` via a large CSS block. Be careful editing the CSS; keep selectors specific to avoid affecting Streamlit internals.
- The sidebar expands on hover; recent fixes ensure the sidebar remains expanded while interacting with select boxes.
- If a dropdown's option menu is rendered outside the sidebar (appended to `body`), a small JS workaround may be required to keep the sidebar open while the menu is visible.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Open a pull request with a clear description of changes

Please follow existing coding style and keep UI/UX changes isolated.

## License

This repository does not include an explicit license file. Add a `LICENSE` file if you plan to publish or distribute the project.

## Contact

For questions or help, open an issue or contact the maintainer listed in project metadata.

--

Updated README: basic setup, run instructions, and development notes.