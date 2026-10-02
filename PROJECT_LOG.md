# Dukaan360 Continuation Log

## Purpose
This file is the durable handoff for any AI or developer continuing the project.

## Product decision
- **Dukaan360 — Sell. Manage. Grow.**
- Android-first merchant app using Expo/React Native; FastAPI backend.
- Prototype integrations are explicitly simulated: payment QR/confirmation, merchant locations, contact actions, and barcode scanning fallback.
- The core story is sale → simulated payment → inventory deduction → refreshed insight.

## Current milestone
**Milestone 1 in progress:** create runnable modular mobile + backend project with seeded data and the complete transaction path.

## Intended commands
```powershell
# Terminal 1
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2
cd mobile
npm install
npx expo start
```

## Rules for future work
- Keep demo payment clearly labelled simulated; do not imply real UPI verification.
- Preserve seeded demo behavior: Milk begins at 5 units so selling 3 visibly triggers a stockout insight.
- Prefer small modules over a monolithic screen or API file.
- Update this log after meaningful changes, including verification status and remaining work.

## Last updated
2026-10-01: Created `backend/` FastAPI prototype and `mobile/` Expo React Native client. The API state is in-memory, seeded with Milk at 5 units. Implemented endpoints and client UI for products, inventory adjustment, sales creation, simulated payment/transaction ID, insight calculation, and merchant opportunities. Core demo interaction is now coded.

### Verification state
- `npm install` completed after an initially partial install; `mobile/package-lock.json` and `node_modules` now exist.
- Expo bundle validation began but did not finish successfully in this environment. Expo SDK 52 reports its Metro packages require Node 18.18+, while this machine has Node 18.16.0. Upgrade Node, run `npm install` again, then use `npx expo start` / `npx expo export --platform android`.
- No usable Python installation was detected (`py --version` reports none), so FastAPI runtime/API testing awaits installation of Python 3.10+.
- No user source files were overwritten; the workspace was initially empty.

### Exact continuation plan
1. Install Python 3.10+ and Node 20 LTS (or Node >=18.18), reopen terminal.
2. From `backend`, make/activate `.venv`, install `requirements.txt`, then launch Uvicorn.
3. From `mobile`, run `npm install`, set `EXPO_PUBLIC_API_URL` to the LAN IP if using Expo Go, then `npx expo start`.
4. Test guided demo: Billing → Demo scan Milk three times → Generate bill → Simulate payment → Inventory (Milk 2) → Insights.
5. If API connection fails on phone, check phone/computer Wi-Fi and Windows firewall port 8000.

### Expo SDK compatibility update
- The installed Expo Go app is SDK 57, while the initial project used SDK 52, causing an incompatibility error.
- On 2026-10-01, `mobile/package.json` was updated to SDK 57-compatible versions: Expo `~57.0.1`, Expo Status Bar `~57.0.0`, React `19.2.3`, and React Native `0.86.0`.
- Expo SDK 57 requires Node >=22.13.0. Upgrade Node first, then from `mobile` run `npm install`, `npx expo install --fix`, `npx expo-doctor`, and finally `npx expo start -c`.
- Diagnostic on 2026-10-01: machine still reports Node `v18.16.0`. An attempted `npm install` therefore encountered a stale SDK 52 tree (`node_modules` / `package-lock.json`) conflicting with the SDK 57 manifest. Do not use `--force` or `--legacy-peer-deps`. Upgrade Node first; then remove only `mobile/node_modules` and `mobile/package-lock.json`, and reinstall cleanly.
- Update later 2026-10-01: Node upgraded successfully to `v24.21.0`, npm to `12.2.0`, and Python `3.14.8` is available. The old `node_modules` cleanup encountered Windows long-path issues in generated React Native debugger assets, but enough was cleared for a fresh SDK 57 install to begin. If npm is interrupted by an editor/tool timeout, run the clean-install commands manually in a normal local PowerShell terminal; do not use `--force`.

### Expanded implementation — product setup and receiving stock
- Added API product creation (`POST /products`), barcode lookup, stock receiving, sales list, and merchant contact simulation.
- Added the Inventory product setup workflow: scan barcode (camera or manual code) → known product opens a quantity-received sheet → unknown product opens a form for barcode, name, price, unit, category, and initial stock.
- Added `expo-camera` SDK 57 dependency and camera permission config. User must run `npx expo install expo-camera` (or `npm install`) after completing base dependency installation.
- Backend accepts manual line items, leaving inventory unchanged for them; billing UI still needs its manual-item form wired to this API improvement.
- Core persistence update: replaced in-memory-only demo storage with standard-library SQLite at `backend/dukaan360.db`. Products/inventory and sales persist through FastAPI restarts. Python syntax verification passed with `py -m compileall backend\\app`.
- Core scanning update: Billing now opens the `expo-camera` barcode scanner and resolves scanned barcodes through the API; an unknown code correctly directs the merchant to first-time product setup in Inventory.

### Customer management implementation
- Added SQLite-backed phone-number customer profiles, persistent due balances, repayment recording, purchase-history favourite-item recommendations, and clearly-disclosed demo engagement reminders.
- API endpoints: `GET/POST /customers`, `POST /customers/{phone}/repay`, `GET /customers/{phone}/recommendations`, `POST /customers/{phone}/engagement`.
- Sales API accepts `customer_phone`, `customer_name`, and `payment_method`; a confirmed `credit` sale increases that customer's balance. Checkout UI wiring for those three fields remains the immediate next task.

### Environment repair — 2026-10-01
- The backend launch originally failed with `ModuleNotFoundError: pydantic_core._pydantic_core`. The venv was usable but its compiled `pydantic-core` binary was missing after a partial install.
- Repaired successfully using `./.venv/Scripts/python.exe -m pip install --upgrade --force-reinstall --no-cache-dir pydantic pydantic-core`.
- Verified API startup successfully with `./.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000`.
- Use the venv Python executable to launch Uvicorn if activation behaves oddly: `./.venv/Scripts/python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`.

### Mobile UI correction — 2026-10-01
- Fixed Customers screen effect bug: `useEffect` no longer returns the Promise from the API loader.
- Restored six bottom-navigation icons using Unicode escape sequences (avoids Windows text encoding corruption), and added a 10px top content inset for Android status-bar clearance.

### Billing/customer completion — 2026-10-01
- Billing now captures customer phone (and new-customer name) before bill creation, supports Pay now and Pay later/credit, and sends those fields to the sale API.
- Confirmed credit sales add to the persistent customer due ledger. Payment confirmation exposes a WhatsApp bill-share deep link for a customer phone.
- Barcode scanner resets its lock state each time it opens; consecutive item scanning is supported by reopening Scan barcode after each product scan.

### Engagement wording update
- Replaced “favourite-item reminder” with professional “buy-again reminder” wording.
- Added a Customer Engagement card at the top of Customers with “Remind all customers to buy again”; it uses a disclosed demo-only bulk-reminder API.

### Requirements audit
- `IMPLEMENTATION_CHECKLIST.md` was created on 2026-10-01. It is the authoritative, candid mapping of the original brief to Done / Partial / Pending work. Read it before claiming the prototype is complete.
