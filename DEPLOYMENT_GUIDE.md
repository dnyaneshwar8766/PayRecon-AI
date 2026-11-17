# PayRecon AI — deployment guide (Render + Vercel)

## 1. Push this project to GitHub
Create a new GitHub repository and upload the contents of this project folder (the folder containing `render.yaml`, `backend/`, and `frontend/`). Do not upload `.venv`, `node_modules`, `.env`, or database files.

## 2. Deploy the API on Render
1. Sign in to https://render.com and choose **New + → Blueprint** (or create a Web Service).
2. Connect the GitHub repository containing this project.
3. If using Blueprint, Render detects the root `render.yaml`. If creating a Web Service manually, set Root Directory `backend`, Build Command `pip install -r requirements.txt`, Start Command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Deploy and wait for the service to become Live.
5. Open `https://YOUR-RENDER-SERVICE.onrender.com/health`; expect JSON with `"status":"ok"`.

## 3. Deploy the frontend on Vercel
1. Sign in to https://vercel.com and choose **Add New → Project**.
2. Import the same GitHub repository.
3. Set Root Directory to `frontend`.
4. Framework preset: Vite. Build command: `npm run build`. Output directory: `dist`.
5. Add environment variable `VITE_API_URL` with the full Render API origin, e.g. `https://YOUR-RENDER-SERVICE.onrender.com` (no trailing slash).
6. Deploy. If you change this variable later, redeploy the frontend.

## 4. Verify
Open the Vercel URL. The dashboard should load sample data. Also verify the Render `/health` endpoint and try a CSV reconciliation.

## Important limitations
- The backend uses SQLite. On Render's ephemeral filesystem, saved history can be lost when the service restarts or redeploys. For persistent history, attach a paid persistent disk and set `PAYRECON_DB_PATH` to a path on that disk, or migrate to managed PostgreSQL.
- This is an assessment/demo app, not a production financial service. It has no authentication, authorization, live bank connection, or production-grade financial data controls.
- The `CORS_ORIGINS` setting is `*` for initial assessment deployment convenience. Before production, set it to the exact Vercel origin and add authentication/security controls.
