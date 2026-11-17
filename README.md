# PayRecon AI — Intelligent Payment Reconciliation Platform

A full-stack, production-inspired final-year project for reconciling payment-platform transactions against bank settlement records.

## What is included

- Premium React + TypeScript + Vite dashboard.
- Python FastAPI reconciliation API.
- Deterministic reconciliation engine (no fake AI decisions).
- Four required discrepancy classes:
  1. Late settlement across a month boundary.
  2. Rounding differences.
  3. Duplicate entries.
  4. Refunds without a matching original transaction.
- CSV import and export.
- Built-in sample dataset generator.
- Automated Python tests.
- Assumptions, API documentation, demo script and production-risk notes.

## Architecture

```text
React / TypeScript dashboard
        |
        | HTTP JSON / CSV
        v
FastAPI backend
        |
        +-- CSV validation and normalization
        +-- deterministic reconciliation engine
        +-- discrepancy classification
        +-- report generation
        |
        v
SQLite run-history persistence (demo scope)
```

The backend deliberately does not claim to use an LLM for financial decisions. Reconciliation is deterministic and auditable. An LLM can be added later for natural-language explanations, but must never decide whether money settled.

## Requirements

- Windows 10/11
- Python 3.10+
- Node.js 20+
- VS Code (recommended)

## Run on Windows

### 1. Start the backend

Open a terminal in the project root:

```bat
cd backend
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend:
- API: http://127.0.0.1:8000
- Interactive API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

### 2. Start the frontend

Open a second VS Code terminal:

```bat
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (usually http://localhost:5173).

## Run automated tests

In a third terminal:

```bat
cd backend
.venv\Scripts\activate
py -m pytest -q
```

## How to use

1. Open the dashboard.
2. Select **Load demo data** to load a reproducible sample.
3. Select **Run reconciliation**.
4. Inspect the discrepancy summary and transaction-level findings.
5. Use **Upload CSVs** to upload your own two files:
   - Platform CSV: `transaction_id, customer_id, transaction_date, amount, currency, type, original_transaction_id`
   - Bank CSV: `bank_entry_id, transaction_id, settlement_date, amount, currency, type, original_transaction_id`
6. Export the reconciliation report as CSV.

`type` should be `payment` or `refund`. Dates should be ISO format (`YYYY-MM-DD`) and amounts should be decimal values.

## Reconciliation assumptions

These assumptions are explicit and configurable in `backend/app/engine.py`:

- Transaction IDs are the primary matching key.
- Currency must match exactly.
- A payment may settle on its transaction date or up to 2 calendar days later.
- A settlement after the transaction month is classified as `late_settlement`, even when it is otherwise a valid match.
- Amount differences up to INR 0.02 are classified as rounding differences; exact tolerance can be changed.
- Exact duplicate bank entries are detected using transaction ID, settlement date, amount, currency and type.
- Refunds are represented as `type=refund`. A refund must reference an original transaction through `original_transaction_id`; if the original transaction is absent from the platform dataset, it is flagged as `unmatched_refund`.
- The engine reports ambiguous matches rather than silently choosing one.
- Completed reconciliation run summaries and results are stored in local SQLite; raw uploaded CSV files are not retained. This does not provide production-grade multi-tenant isolation.

## Important production limitations

1. Bank files can contain reversals, fees, chargebacks, partial settlements, split settlements and timezone differences that this starter schema does not fully model; treating them as ordinary payments could create false discrepancies.
2. Matching by transaction ID assumes both providers preserve a common identifier; real integrations often require provider-specific reference mapping and carefully governed fuzzy matching with human review.
3. The sample app has only local SQLite run history and no immutable audit ledger, encryption/key management, role-based approval workflow or production monitoring; these are mandatory before handling real financial data.

## Assessment evidence checklist

- [ ] Preserve the real brainstorming conversation (the prepared planning note in `docs/BRAINSTORMING_RECORD.md` is not a verbatim chat export).
- [ ] Save the exact distilled prompt and raw prompt actually used in the AI coding tool; `docs/RAW_PROMPT_TEMPLATE.md` contains a ready-to-use prompt, not evidence that it was submitted.
- [ ] Export the actual AI coding execution thread, including debugging turns; this project was not built inside the user's Claude Code account, so no Claude Code transcript can be truthfully supplied.
- [ ] Run tests locally and keep terminal output/screenshots; do not submit a screenshot unless it is captured from your own run.
- [ ] Record a demo showing sample import, reconciliation, discrepancy drill-down and CSV export.
- [ ] Deploy only after adding secrets/configuration and testing the deployed backend. A live deployment is not included in this ZIP.
- [ ] Do not claim deployment or test success until actually verified.

## Suggested demo video flow (3–4 minutes)

1. Introduce the problem and explain why platform records and bank settlement records differ.
2. Load the generated sample data.
3. Run reconciliation.
4. Show one example of each discrepancy class.
5. Upload a CSV and explain the required schema.
6. Export the report.
7. Show the automated test results and explain the production limitations.

## Run history persistence

The backend stores each completed reconciliation run in a local SQLite database at `backend/payrecon.db` (created automatically). History endpoints:
- `GET /api/runs?limit=20` — latest run summaries.
- `GET /api/runs/{run_id}` — complete saved result.

Set `PAYRECON_DB_PATH` to choose another database file. This local SQLite history is suitable for a project demo, not a production multi-user financial ledger.
