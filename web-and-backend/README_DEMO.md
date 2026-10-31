# MandiMitra Demo Website + FastAPI Backend

This package contains a working frontend demo connected to the MandiMitra FastAPI backend.

## Run on macOS

### 1. Start the backend

Open Terminal in the `backend` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your data.gov.in API key to `.env` (do not put it in frontend files or commit `.env`).

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Backend runs at `http://127.0.0.1:8000`.

### 2. Start the website

Open a second Terminal window, go to the `frontend` folder:

```bash
python3 -m http.server 3000
```

Open `http://127.0.0.1:3000`.

The backend CORS settings already allow localhost:3000 for local development.

## Demo mode

If the data.gov.in API key is not configured or the live API is unavailable, click **“Or explore with sample data”**. The site then uses clearly labelled illustrative sample records so you can demonstrate the user flow. Sample values are NOT live mandi prices and must not be presented as real data.

## Included workflow

1. Enter crop, state, district and quantity.
2. Load mandi records from `GET /api/v1/mandi-prices`.
3. Enter transport and other expenses for each market.
4. Compare using `POST /api/v1/compare`.
5. View the ranked estimated net return.

## Important

- The frontend does not contain the data.gov.in API key.
- The backend calculates the authoritative comparison; live mode does not calculate net return in the browser.
- Prices are indicative reported modal prices, not guaranteed selling prices.
- The language selector is currently a UI preview; translations are not yet implemented.
- The site is a local hackathon demo, not a production deployment.


## In-app MandiMitra Guide (new)
The frontend now shows a small welcome notification shortly after opening. A floating
“Ask MandiMitra” button opens a help panel with suggested questions and answers about:
- finding mandi prices and comparing markets;
- adding transport and other expenses;
- understanding estimated net return;
- trying sample mode and connecting live data.

This is currently a lightweight, rule-based demo assistant. It works without a paid
AI subscription or API key, but it is not yet a connected generative-AI model. It does
not fetch prices or make selling decisions. A real AI integration can be added later
through a backend endpoint, with verified mandi data supplied as context.
