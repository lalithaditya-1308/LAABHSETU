# LAABHSETU — Web + Android starter (v1)

Laabhsetu helps farmers compare reported mandi modal prices after estimated transport and other expenses. This release contains a responsive web app, the existing FastAPI backend, a multilingual Mitra assistant interface, and an Expo Android wrapper.

## What's included

- Responsive web frontend with a farmer-first dashboard.
- Language selector: English, Hindi and Telugu (Telugu is prioritised as the third language).
- Mitra assistant panel with welcome notification, suggested prompts, chat UI and browser speech input (Chrome support varies by device/language).
- Assistant API endpoint: `POST /api/v1/assistant/chat`.
- Optional real AI connection through backend environment variables. Without an AI key, the endpoint returns safe guided fallback help; the UI also has local fallback help if the backend is offline.
- Existing mandi-price connector and expense-aware net-return comparison.
- Android app source using Expo + WebView to run the same responsive app.

## 1. Run the backend on Mac

```bash
cd web-and-backend/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your data.gov.in API key to `backend/.env` for live mandi data. For a real generative assistant, optionally add an AI API key and model settings there too:

```env
AI_API_KEY=your_key_here
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
```

Never put API keys in frontend JavaScript or commit `.env` to GitHub.

Start the API:

```bash
uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000` · Docs: `http://127.0.0.1:8000/docs`

## 2. Run the web app

Open a second Terminal window:

```bash
cd web-and-backend/frontend
python3 -m http.server 3000
```

Open `http://127.0.0.1:3000` in Chrome or Safari.

Use the language selector in the top bar to switch English / हिन्दी / తెలుగు. The microphone button uses browser speech recognition where supported; Chrome is recommended. Voice recognition requires browser support and may require microphone permission.

## 3. Run Android app

Install Node.js first, then:

```bash
cd android
npm install
npx expo start
```

- Android emulator: default URL `http://10.0.2.2:3000` points to your Mac's local web server.
- Physical Android phone: set `EXPO_PUBLIC_WEB_URL` to your Mac's LAN IP, for example `http://192.168.1.10:3000`, and ensure the phone and Mac share the same Wi-Fi. Keep the backend CORS origin configured for the frontend host.
- Deployed app: set `EXPO_PUBLIC_WEB_URL` to your deployed HTTPS website URL.

To create an installable internal APK (requires an Expo/EAS account and Android build setup):

```bash
npx eas-cli login
npx eas-cli build:configure
npx eas-cli build --platform android --profile preview
```

The EAS project ID in `android/app.json` is a placeholder; `eas build:configure` will initialise your project and provide the correct project ID. The build service will produce an APK when the build completes. This source package does not contain a prebuilt APK.

## 4. Assistant behaviour and safety

- Mitra sends a user's question, selected language and limited page context to `/api/v1/assistant/chat`.
- If `AI_API_KEY` is configured, the backend calls an OpenAI-compatible Chat Completions endpoint. Keep keys server-side.
- Without an AI key, the backend responds with short multilingual guidance. This fallback is not a generative model.
- The assistant is instructed not to invent mandi prices, dates, distances or buyer availability. It must use supplied comparison context and say when information is missing.
- Prices are indicative reported modal prices. Actual sale price depends on crop quality, grade, arrivals and buyers. Net return is an estimate, not a profit guarantee.

## 5. Demo mode and live data

Click “Or explore with sample data” if the API key is not configured or live data is unavailable. Sample records are illustrative only and must not be presented as live mandi prices.

## Current limitations / next production steps

- The Android project is a WebView app wrapper around the responsive web product, not a fully native offline-first rewrite.
- Configure production HTTPS hosting, CORS, secure secret management and a real database before public launch.
- Verify the data.gov.in resource, query filters, rate limits and latest available records in the target states.
- Complete native speech support and professional review of Telugu/Hindi agricultural terminology.
- Add authentication, saved farmer profiles, price history, push notifications, accessibility testing and field testing with farmers.
- The current app is a development/hackathon starter, not a production financial or agricultural advisory service.
