# MandiMitra Backend

FastAPI backend starter for an expense-aware mandi price comparison app.

## What is included

- `GET /api/v1/health` — backend status and API-key configuration status.
- `GET /api/v1/crops` — starter crop list.
- `GET /api/v1/locations` — location endpoint placeholder.
- `GET /api/v1/mandi-prices?commodity=Wheat&state=Uttar%20Pradesh` — fetch and normalize mandi prices.
- `POST /api/v1/compare` — compare estimated net returns after user-entered expenses.
- Automatic request validation through Pydantic.
- Invalid/missing modal prices are rejected rather than silently changed to zero.
- Old records are marked stale based on `STALE_AFTER_DAYS`.

## Data source

The connector uses the data.gov.in resource for **Current Daily Price of Various Commodities from Various Markets (Mandi)**, generated through AGMARKNET.

Resource ID: `9ef84268-d588-465a-a308-a864a43d0070`

Official dataset: https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi

Prices are daily reported wholesale market prices, not guaranteed real-time bids or guaranteed sale prices. The app must display source and arrival date.

## Setup on macOS

Open Terminal in this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and replace `put_your_own_key_here` with your own data.gov.in API key.

Never commit `.env` or expose the key in frontend code.

Run the server:

```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

## Test

```bash
pytest -q
```

## Example price request

```bash
curl "http://127.0.0.1:8000/api/v1/mandi-prices?commodity=Wheat&state=Uttar%20Pradesh"
```

## Example comparison request

First call `/api/v1/mandi-prices` and copy exact market names from its results. Then send those names and the expenses:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "commodity": "Wheat",
    "state": "Uttar Pradesh",
    "district": "Prayagraj",
    "quantity_quintals": 20,
    "costs": [
      {"market": "EXACT MARKET NAME A", "transport_cost": 3000, "other_expenses": 1000},
      {"market": "EXACT MARKET NAME B", "transport_cost": 1000, "other_expenses": 0}
    ]
  }'
```

The market names above are placeholders. Use exact names returned by the price endpoint.

## Calculation

- Gross revenue = modal price per quintal × quantity in quintals
- Total expenses = transport cost + other expenses
- Estimated net return = gross revenue − total expenses

This is an estimate using the reported modal price and expenses entered by the user. It is not guaranteed profit.

## Important MVP limitations / next work

1. Confirm the API key and live response from your account.
2. Verify API filter field names against the live resource's API page; government schemas can change.
3. Implement pagination if your selected crop/state has more records than the configured page size.
4. Populate crops and locations from verified source records instead of the starter crop list.
5. Add persistent caching/database and scheduled refresh if required.
6. Add AI only after deterministic price retrieval and calculation work reliably. AI must explain verified backend results, never invent prices or calculate authoritative totals.
7. Restrict CORS to the deployed frontend origin before production.

## Comparison calculation implementation

The calculation logic is in `app/services/calculations.py`:

- `compute_option(...)` validates the four financial inputs and uses `Decimal` internally.
- `rank_options(...)` sorts by estimated net return (descending), then transport cost (ascending).
- `app/services/calculation_service.py` connects those functions to the mandi-price records and the existing `POST /api/v1/compare` route.

Run the unit and service/API tests from the project root:

```bash
python3 -m pytest -v
```

The comparison endpoint only calculates markets for which the request includes an expense entry. It matches market names without case sensitivity and returns the source date/staleness information with each result.
