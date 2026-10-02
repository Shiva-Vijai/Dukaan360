# Render Deployment

This guide deploys the FastAPI service in `backend/` as a Render Free Web Service and connects the standalone Android build to its HTTPS URL.

## Render service settings

The repository includes `render.yaml`, so the service can be created from the Render Blueprint flow with these values:

- **Service type:** Web Service
- **Name:** `dukaan360-api`
- **Runtime:** Python
- **Plan:** Free
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path:** `/health`
- **Environment variable:** `CORS_ALLOWED_ORIGINS=*`

Render provides `PORT` automatically. The service must bind to `0.0.0.0`; do not replace it with a local address.

## Deploy from GitHub

1. Push this repository to GitHub, including `render.yaml`, `backend/requirements.txt`, and the `backend/app/` package.
2. In the Render dashboard, select **New > Blueprint**.
3. Connect the GitHub repository and select the branch to deploy.
4. Review the service settings generated from `render.yaml`.
5. Create the Blueprint and wait for the first deploy to finish.
6. Copy the public service URL, for example `https://dukaan360-api.onrender.com`.

The final API base URL is:

```text
https://YOUR-SERVICE-NAME.onrender.com
```

## Verify the deployment

Open this URL in a browser or run:

```powershell
Invoke-RestMethod https://YOUR-SERVICE-NAME.onrender.com/health
```

Expected response:

```json
{"status":"ok"}
```

## SQLite and Render Free

The backend currently stores products, sales, and customers in `dukaan360.db`. The path can be changed with `DUKAAN_DB_PATH`.

Render Free services use an ephemeral filesystem. The SQLite file will survive normal requests while the instance is running, but it can be deleted when Render restarts, redeploys, or spins down the service. This means inventory, sales, and customer records are not production-persistent on the Free plan.

For durable production data, use an external managed PostgreSQL-compatible database and migrate the repository layer, or use a Render persistent disk on a plan that supports it. This deployment does not silently claim SQLite persistence.

## CORS

The default `CORS_ALLOWED_ORIGINS=*` is suitable for the native React Native client because it does not rely on browser-origin restrictions. For browser clients, set a comma-separated list instead, for example:

```text
CORS_ALLOWED_ORIGINS=https://your-frontend.example,https://admin.example
```

## Local backend verification

From the repository root:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

In another terminal:

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/products
```

## Connect the mobile application

For local development, create `mobile/.env` from `mobile/.env.example` and set the computer's LAN address:

```text
EXPO_PUBLIC_API_URL=http://192.168.1.x:8000
```

For EAS builds, create the public API URL in the EAS environment used by the build. After the Render URL is known:

```powershell
cd mobile
eas env:create --environment preview --name EXPO_PUBLIC_API_URL --value https://YOUR-SERVICE-NAME.onrender.com --visibility plaintext
eas env:create --environment production --name EXPO_PUBLIC_API_URL --value https://YOUR-SERVICE-NAME.onrender.com --visibility plaintext
```

`EXPO_PUBLIC_API_URL` is not a secret; it is embedded into the mobile bundle at build time. Do not put API keys or private credentials in it.
