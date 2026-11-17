# PayRecon AI — brainstorming record

> Evidence note: this is a structured planning record prepared from the assignment brief and the implementation decisions. It is **not** a verbatim export of a complete LLM chat. The assessment asks for the full original conversation; attach/export the actual chat history separately if your evaluator requires literal conversation evidence.

## Problem framing
**Question:** How can a finance team explain a month-end difference between payment-platform transactions and bank settlements?

**Initial observation:** The two datasets describe related events at different points in the payment lifecycle. The platform records the customer's payment immediately; the bank records a later settlement batch. Comparing totals alone cannot explain which transactions caused a difference.

## Candidate approaches considered
1. **Aggregate-only comparison:** compare daily/monthly totals. Simple, but cannot identify the exact transaction responsible for a gap.
2. **Exact row matching:** join by transaction ID and compare amounts. Explainable, but misses settlement timing and duplicate/refund edge cases.
3. **Rule-based reconciliation with exception categories:** normalize both datasets, match by stable identifiers, compare amounts/dates/types, and return transaction-level findings. Chosen because it is deterministic, auditable, and easy to test.
4. **LLM decides whether a transaction matched:** rejected for the core financial decision because probabilistic output is difficult to audit and can invent a match. An LLM could later summarize already-computed findings, with deterministic rules remaining authoritative.

## Chosen solution
Build PayRecon AI with a React + TypeScript dashboard and a Python FastAPI service. The engine performs deterministic matching and emits structured issue codes. The UI supports generated sample data, CSV upload, filtering, discrepancy review, and CSV report export. Completed run summaries/results are persisted in a local SQLite database for demo history.

## Explicit assumptions
- `transaction_id` is the primary matching key.
- A normal settlement occurs on the transaction date or within two calendar days.
- A payment settling in a later calendar month is flagged even if it is otherwise matched.
- A difference of up to INR 0.02 is classified as a rounding difference.
- Exact duplicate bank rows are detected by transaction ID, settlement date, amount, currency, and type.
- Refunds carry an `original_transaction_id`; missing original platform transactions are flagged.
- Ambiguous matches are sent for review instead of silently selecting a winner.

## Why these decisions
The chosen approach explains each discrepancy at row level, keeps the financial decision reproducible, and makes the assumptions testable. It also avoids claiming that a generative model can prove whether money settled.

## Trade-offs and unresolved production questions
- Real providers may use different references, split one payment into multiple settlements, net fees, or issue reversals/chargebacks.
- Calendar-day logic is a simplification; bank cut-off times, holidays and timezones matter.
- A fixed INR tolerance is only a demo assumption; currency-specific decimal precision and provider rules are required.
- SQLite run history is suitable for a local demo, not concurrent multi-tenant financial operations.
