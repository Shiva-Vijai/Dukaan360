# Dukaan360 Requirements Checklist

Status legend: **Done** = coded in the current source; **Partial** = some of the workflow exists but not the complete requirement; **Pending** = not yet coded or verified.

## Product and UX

- [x] **Done** Android-first Expo / React Native app structure.
- [x] **Done** Bottom navigation: Home, Billing, Inventory, Insights, Network.
- [x] **Done** Professional, restrained merchant/fintech visual direction.
- [x] **Done** Seeded grocery products and deterministic demo behaviour.
- [ ] **Pending** Offline local queue and backend sync when internet returns.
- [ ] **Pending** Authentication / merchant profiles (intentionally low priority for the hackathon).

## Dashboard

- [x] **Done** Today's sales, bills, product count, low-stock count.
- [x] **Done** Dashboard smart-action cards derived from API insights.
- [x] **Done** Navigation from dashboard to billing and insights.

## Product catalogue and onboarding

- [x] **Done** Seeded product catalogue with barcode, category, price, unit, quantity, and demand rate.
- [x] **Done** Barcode lookup API: `GET /products/barcode/{barcode}`.
- [x] **Done** Product creation API: `POST /products`.
- [x] **Done** Inventory UI flow for an unknown barcode: barcode → name, rate, unit, category, initial stock → save.
- [x] **Done** Inventory UI flow for a known barcode: barcode → incoming quantity → inventory update.
- [x] **Done** Manual barcode-code fallback in the scanner screen.
- [x] **Done (requires dependency install)** Camera scanner component using `expo-camera`.
- [ ] **Pending** Product edit/delete UI and duplicate-barcode recovery UI.

## Billing

- [x] **Done** Product search and cart creation from seeded catalogue.
- [x] **Done** Cart quantity increase/decrease, line totals, total, and removal at zero quantity.
- [x] **Done** Generate a pending bill in FastAPI.
- [x] **Done** Inventory is checked before sale creation.
- [x] **Done (requires dependency install)** Billing uses the real camera/manual barcode scanner and looks up scanned products by barcode.
- [ ] **Pending** Billing UI for loose/manual items; backend support exists for manual item name, unit price, and quantity, but the form is not yet wired into the client.
- [ ] **Pending** Separate invoice/receipt history UI.

## Payment prototype

- [x] **Done** Bill-linked amount on payment screen.
- [x] **Done** Deterministic visual demo QR.
- [x] **Done** Clearly labelled simulated payment confirmation.
- [x] **Done** Generated `D360-TXN-*` transaction ID.
- [x] **Done** Payment status changes from pending to completed.
- [x] **Done** Explicit wording that no real UPI transaction occurs.
- [ ] **Pending by design** Real payment gateway, bank integration, webhooks, or actual transaction verification.

## Automatic inventory

- [x] **Done** Inventory only deducts after simulated payment confirmation.
- [x] **Done** Completed sale deducts each stocked sale item.
- [x] **Done** Manual/non-catalogue API sale items do not alter inventory.
- [x] **Done** Inventory refreshes after payment confirmation.
- [x] **Done** Inventory search, price, quantity, category, barcode, and status display.
- [x] **Done** Status labels: Healthy, Low Stock, Critical, Overstock, Slow Moving.
- [x] **Done** Add-stock UI and API.

## Intelligence

- [x] **Done** Explainable average-demand / days-remaining calculation.
- [x] **Done** Stockout risk and restock recommendation card.
- [x] **Done** Excess-stock card for Cooking Oil.
- [x] **Done** Slow-moving-stock card for Premium Biscuits.
- [x] **Done** Dashboard and dedicated insights presentation.
- [ ] **Partial** Historical sales data is represented by seeded demand parameters, not a generated 30-day sale dataset/chart.
- [ ] **Pending** Pandas/scikit-learn analytics layer; current rules are intentionally simple FastAPI calculations.

## Merchant-to-merchant network

- [x] **Done** Seeded Ravi Stores and Lakshmi Mart opportunities.
- [x] **Done** Product, estimated need, excess quantity, and simulated distance display.
- [x] **Done** Contact button with a no-real-message disclosure.
- [x] **Done** Contact simulation API: `POST /merchant-network/{id}/contact`.
- [ ] **Partial** Opportunity list is deterministic seed data, not dynamically recalculated from a full multi-merchant inventory dataset.
- [ ] **Pending by design** GPS, real merchant onboarding, stock transfer, sale negotiation, or real messaging.

## Customer management and money management

- [x] **Done** Phone-number customer profiles persisted in SQLite.
- [x] **Done** Customer creation and customer list API/UI.
- [x] **Done** Customer outstanding balance (`due`) tracked in SQLite.
- [x] **Done** Repayment recording API/UI, which reduces the outstanding balance.
- [x] **Done** Customer purchase-history recommendation API for favourite / usually bought items.
- [x] **Done** Clearly-disclosed simulated favourite-item reminder API/UI; no SMS/WhatsApp/push is actually sent.
- [x] **Done** Credit-sale API support: a sale can be linked to a customer phone and marked `payment_method: credit`; payment confirmation adds its total to the customer's due balance.
- [ ] **Partial** Checkout UI has not yet exposed the customer-phone and credit-payment selector, though the API contract is ready. This is the next required UI wiring task.
- [ ] **Pending** Scheduled/random production notifications and consent management. These need a real notification provider and opt-in records; prototype only prepares a disclosed demo reminder.

## Backend/data architecture

- [x] **Done** Modular FastAPI project and CORS setup.
- [x] **Done** Product, inventory, sales, payment, analytics, and merchant-network endpoints.
- [x] **Done** Health endpoint and demo reset endpoint.
- [x] **Done** SQLite persistence: product inventory and completed/pending sales are saved in `backend/dukaan360.db` and survive API restarts.
- [x] **Done** SQLite is the local-development database.
- [ ] **Pending** PostgreSQL configuration/models/migrations for production.
- [ ] **Pending** Environment variable configuration beyond mobile API URL.

## Verification / run readiness

- [x] **Done** Node 24.21, npm 12.2, and Python 3.14.8 were detected on this computer.
- [ ] **Pending** Clean `npm install` completion after the Node upgrade; old generated dependencies caused Windows long-path cleanup trouble.
- [ ] **Pending** `npx expo-doctor` verification.
- [ ] **Pending** Expo Go device run and camera permission test.
- [ ] **Pending** FastAPI server/API end-to-end test.
- [ ] **Pending** Full demo script run: scan/set up → bill → simulated payment → deduction → insight → network opportunity.

## Priority remaining work

1. Complete a clean SDK 57 dependency install, including `expo-camera`, and verify Expo Go launches.
2. Run FastAPI and test the full scan → bill → payment → SQLite persistence flow on device.
3. Wire the loose-item form into Billing (manual-item backend support already exists).
4. Add PostgreSQL configuration/models/migrations if production persistence is needed.
5. Generate historical sales/merchant data and make opportunity matching dynamic.
