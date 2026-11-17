# Raw prompt for an AI coding tool — ready to submit

> This is a prepared prompt based on the assessment requirements. It is **not evidence of the exact prompt previously submitted** to Claude Code, Cursor, or Lovable. If you use it, preserve the actual submitted text and tool history.

```text
Build PayRecon AI, a complete, polished payment reconciliation web application for the Onelab AI Fitness Assessment. The business problem: a payments platform records customer transactions immediately, while the bank batches and settles funds 1–2 days later. At month end, the platform and bank totals do not match; the system must identify exactly why and show the affected records.

Create synthetic but realistic platform_transactions.csv and bank_settlements.csv data yourself. The dataset must deliberately include all four required cases: (1) a transaction from the last day(s) of a month settling in the following month, (2) small per-transaction rounding differences whose aggregate impact is visible in totals, (3) a duplicate row in one dataset, and (4) a refund with no matching original transaction. Include normal exact matches and at least one bank-only or platform-only record for meaningful reconciliation.

Build a full-stack app using React + TypeScript + Vite for the frontend and Python FastAPI for the backend. Provide a premium, responsive finance dashboard. Include CSV upload for both datasets, schema validation, sample-data loading, deterministic reconciliation, transaction-level findings with clear reasons, summary totals, issue filters/search, reconciliation run history, and CSV report export. Add a documented API and Windows setup instructions.

Core reconciliation must be deterministic and auditable, not an LLM guessing whether money settled. Use explicit issue codes for late_settlement, rounding_difference, duplicate_bank, unmatched_refund, and other useful mismatches. Send ambiguous matches to manual review; never silently choose one. State every assumption, including matching key, settlement window, month-boundary treatment, rounding tolerance, duplicate definition, refund linkage, and handling of ambiguous matches. Use decimal-safe money arithmetic.

Write automated tests for all required cases plus exact match, amount mismatch, invalid input, currency mismatch, and ambiguous match. Run the tests and report only results actually observed. Do not invent deployment URLs, screenshots, test results, user accounts, or AI conversation transcripts. Include a README, architecture description, test plan, assumptions log, demo script, and three concise sentences about production risks. Keep the implementation runnable and explain any incomplete verification honestly.
```
