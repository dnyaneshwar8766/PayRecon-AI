# Demo narration

**Opening:** PayRecon AI helps finance teams understand why payment-platform records and bank settlements do not reconcile at month end.

**Import:** I will load the provided sample data. The platform records a payment immediately, while the bank may settle it later.

**Run:** The reconciliation engine normalizes both files and matches using transaction ID, currency, type and amount. It reports ambiguous records rather than silently selecting a match.

**Findings:** The demo includes a next-month settlement, a one-paise rounding difference, a duplicated bank entry, and a refund whose original transaction is absent. Each finding includes a reason.

**Evidence:** I can filter transactions and export the current results to CSV. Automated tests cover the core scenarios and invalid inputs.

**Limitations:** Before production, we need richer settlement models, persistent audit records, security controls, provider adapters and operational monitoring.
