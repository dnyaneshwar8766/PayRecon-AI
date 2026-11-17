# Reconciliation assumptions and decision log

| Area | Assumption | Reason | Risk |
|---|---|---|---|
| Primary key | transaction_id | Deterministic traceability | IDs may differ across processors |
| Settlement window | 0–2 calendar days | Based on assessment description | Weekends, holidays and cut-off times may extend it |
| Month boundary | Later calendar month is flagged | Required scenario | Timezones and accounting cut-offs may differ |
| Rounding | Absolute per-transaction difference <= 0.02 is classified as rounding; the report totals expose cumulative drift across rows | Small tolerance for demo INR data | Currency/provider-specific precision varies |
| Duplicate | Exact transaction/date/amount/currency/type key | Avoids collapsing legitimate partial settlements | Real bank exports may use distinct references |
| Refund | Explicit type=refund and original_transaction_id | Makes refund lineage auditable | Partial and multiple refunds need a richer model |
| Ambiguity | More than one candidate is sent to review | Avoids silently choosing a record | Requires human workflow |
| Persistence | Completed run summaries and results are stored in local SQLite; uploaded source files are not retained | Gives the demo a basic run-history view without retaining raw financial uploads | Local SQLite is not a production multi-tenant ledger; retention, encryption, access control and audit immutability are not implemented |

## Future engineering work

- Provider-specific bank adapters and reference mapping.
- Split settlements, fees, chargebacks, reversals and partial refunds.
- Currency-aware decimal precision and FX conversion.
- Timezone-aware settlement cut-off rules.
- Immutable audit log and approval workflow.
- Database persistence, tenant isolation, encryption and access controls.
