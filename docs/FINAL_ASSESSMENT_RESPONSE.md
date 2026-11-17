# Onelab AI Fitness Assessment — PayRecon AI

## Solution summary
PayRecon AI reconciles payment-platform transactions against bank settlement records and explains the month-end gaps at transaction level. It uses a deterministic, auditable Python reconciliation engine behind a React dashboard. The engine identifies next-month settlements, cumulative rounding drift, duplicate bank entries, unmatched refunds, and additional mismatches such as amount/currency errors and ambiguous matches.

## Data generated
The project includes synthetic platform and bank CSV datasets. The generated sample deliberately contains the four scenarios named in the brief, alongside ordinary matches and a bank-only entry.

## Method
The engine normalizes the two sources, groups records by transaction ID, checks transaction type/currency/amount/date, detects exact duplicate bank rows, and reports explicit issue codes with explanations. It uses Decimal arithmetic for money and sends ambiguous cases to review rather than guessing.

## Assumptions
See `ASSUMPTIONS.md`. The key assumptions are a 0–2 calendar-day normal settlement window, flagging a payment that settles in a later calendar month, INR 0.02 rounding tolerance, exact duplicate-key detection, and refund linkage through `original_transaction_id`.

## Verification
The backend test suite passed 8 tests in the build environment. The Python modules compiled and the ZIP archive passed integrity checking. Frontend dependency installation timed out in the build environment, so a local `npm install` and `npm run build` are still required before claiming full frontend build verification.

## Production risks (three sentences)
See `PRODUCTION_RISK_ANSWER.md`; the three-sentence answer is reproduced there for direct use.

## Working output and evidence
- Code package: `PayRecon_AI_Final_Year_Project.zip`.
- Local run instructions: `../README.md`.
- Demo narration: `DEMO_SCRIPT.md`.
- Deployment URL: not included; deploy and verify the app before entering a live URL.
- Demo video: not included; record the running app using the script.
- Actual brainstorming and coding-tool transcripts: not fabricated; attach the original exported conversations.
