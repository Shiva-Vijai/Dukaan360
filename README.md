# Dukaan360

**Sell. Manage. Grow.**

Dukaan360 is an Android merchant operations app for fast billing, inventory control, stock intelligence, and local business networking. It brings the daily workflow of a small retailer into one focused interface: scan a product, create a bill, confirm payment, update stock, and act on useful recommendations.

## Install the Android app

Download the standalone Android APK directly from this repository:

[Download Dukaan360 APK](https://github.com/Shiva-Vijai/Dukaan360/raw/refs/heads/main/Dukaan360.apk)

Open the downloaded file on an Android phone and approve installation from this source when Android requests permission. This build connects to the deployed API at `https://dukaan360-backend-service.onrender.com` and does not require Expo Go.

## Capabilities

- **Billing:** Search the catalogue or scan a barcode to build a cart and create a sale.
- **Barcode onboarding:** Register an unknown barcode once, then use it for future billing and stock receiving.
- **Inventory:** View stock, pricing, categories, barcode identifiers, and stock health; receive incoming quantities without overwriting current stock.
- **Payment confirmation:** Complete a bill through a clearly separated payment-provider boundary before inventory is deducted.
- **Stock intelligence:** See explainable stockout, overstock, and slow-moving recommendations based on demand and current quantities.
- **Merchant network:** Discover nearby inventory opportunities and send simulated contact requests.
- **Durable local data:** Products and sales are persisted in SQLite across backend restarts.

## Product workflow

1. Scan or search for a product in **Billing**.
2. Add quantities and create a pending bill.
3. Confirm payment through the payment flow.
4. Deduct inventory only after payment completion.
5. Review refreshed inventory and stock recommendations.

The included payment provider is a local development implementation: it records a simulated confirmation and transaction ID, but does not move money or connect to a live UPI provider. This boundary is ready to be replaced by a regulated payment integration.

## Technology

- **Mobile:** Expo SDK 57, React Native, React 19, and `expo-camera`
- **API:** FastAPI with Uvicorn
- **Persistence:** SQLite
- **Runtime:** Python 3.10+ and Node.js 22.13+

## Getting started

### 1. Start the API

From the repository root, open a terminal and run:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Verify the API at <http://localhost:8000/health>. A successful response is:

```json
{"status":"ok"}
```

### 2. Start the mobile application

In a second terminal:

```powershell
cd mobile
npm install
npx expo start
```

Open the app with Expo Go on an Android device or emulator.

### Physical Android device

The phone cannot use `localhost` to reach the computer. Find the computer's Wi-Fi IPv4 address with `ipconfig`, then start Expo with that address:

```powershell
cd mobile
$env:EXPO_PUBLIC_API_URL="http://YOUR_LAN_IP:8000"
npx expo start --clear
```

The phone and computer must be on the same network, and Windows Firewall must allow Python/Uvicorn to accept connections on port `8000`.

For an Android emulator, use `http://10.0.2.2:8000` instead.

## API surface

The FastAPI service exposes the following resource groups:

| Area | Endpoints |
| --- | --- |
| Health | `GET /health` |
| Products | `GET /products`, `GET /products/barcode/{barcode}`, `POST /products` |
| Inventory | `POST /inventory/{product_id}/add` |
| Sales | `GET /sales`, `POST /sales` |
| Payments | `POST /payments/simulate/{sale_id}` |
| Analytics | `GET /analytics/dashboard`, `GET /analytics/insights` |
| Merchant network | `GET /merchant-network/opportunities`, `POST /merchant-network/{opportunity_id}/contact` |

## Repository structure

```text
backend/
	app/
		data.py       SQLite repository and product data
		main.py       FastAPI routes and business operations
		schemas.py    Request validation models
	requirements.txt
mobile/
	App.js          Application shell and navigation
	src/
		api.js        API client
		store.js      Shared application state
		components/  Reusable UI and barcode scanner
		screens/     Billing, inventory, insights, dashboard, and network views
```

## Data and configuration

The local database is created at `backend/dukaan360.db` on first API startup. It stores the product catalogue, inventory quantities, and sales. Restarting the API does not reset this data.

The mobile API base URL is read from `EXPO_PUBLIC_API_URL`. When it is not set, the app falls back to `http://localhost:8000`, which is appropriate for a local simulator but not a physical phone.

## Render and Android release builds

Render deployment settings, SQLite persistence limitations, and the GitHub deployment flow are documented in [DEPLOY_RENDER.md](DEPLOY_RENDER.md). The Render Blueprint is available in [render.yaml](render.yaml).

After setting `EXPO_PUBLIC_API_URL` to the deployed HTTPS API URL in the EAS `preview` or `production` environment, build the mobile application with:

```powershell
cd mobile
npm install -g eas-cli
eas login
eas build:configure
eas build -p android --profile preview
```

The `preview` profile produces an installable APK. Use the `production` profile for a Play Store App Bundle:

```powershell
eas build -p android --profile production
```

## Security and deployment notes

This repository is configured for local development and evaluation. Before a production deployment:

- replace the local payment provider with a regulated payment gateway and server-side transaction verification;
- add authentication, authorization, rate limiting, and audit logging;
- move persistence to a managed database with migrations and backups;
- serve the API over HTTPS and manage secrets through environment configuration;
- add automated tests and a release build pipeline for the mobile application.

