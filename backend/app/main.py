from __future__ import annotations
import csv, io, os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .engine import reconcile
from .sample_data import sample_rows
from .storage import initialize, save_run, list_runs, get_run

app = FastAPI(title="PayRecon AI API", version="1.0.0",
              description="Deterministic payment reconciliation and discrepancy detection API.")
initialize()

app.add_middleware(
    CORSMiddleware, allow_origins=[origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()],
    allow_credentials=False, allow_methods=["*"], allow_headers=["*"]
)

class ReconcileRequest(BaseModel):
    platform: list[dict] = Field(default_factory=list)
    bank: list[dict] = Field(default_factory=list)

@app.get("/health")
def health():
    return {"status":"ok", "service":"PayRecon AI API", "version":"1.0.0"}

@app.get("/api/sample")
def get_sample():
    return sample_rows()

@app.post("/api/reconcile")
def run_reconciliation(payload: ReconcileRequest):
    try:
        result = reconcile(payload.platform, payload.bank)
        result["run"] = save_run(result, "api")
        return result
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

def read_csv(upload: UploadFile) -> list[dict]:
    try:
        raw = upload.file.read().decode("utf-8-sig")
        if len(raw) > 10_000_000:
            raise ValueError("CSV exceeds 10 MB limit.")
        reader = csv.DictReader(io.StringIO(raw))
        if not reader.fieldnames:
            raise ValueError("CSV must contain a header row.")
        return [dict(row) for row in reader]
    except UnicodeDecodeError:
        raise ValueError("CSV must be UTF-8 encoded.")

@app.post("/api/reconcile/upload")
async def upload_and_reconcile(platform_file: UploadFile = File(...), bank_file: UploadFile = File(...)):
    if not platform_file.filename.lower().endswith(".csv") or not bank_file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=415, detail="Upload two .csv files.")
    try:
        platform_rows = read_csv(platform_file)
        bank_rows = read_csv(bank_file)
        result = reconcile(platform_rows, bank_rows)
        result["run"] = save_run(result, "csv_upload")
        return result
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@app.get("/api/runs")
def reconciliation_history(limit: int = 20):
    return {"runs": list_runs(limit)}

@app.get("/api/runs/{run_id}")
def reconciliation_run_detail(run_id: int):
    result = get_run(run_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Reconciliation run not found")
    return result
