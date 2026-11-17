# Three-sentence production-risk answer

1. Real bank feeds can contain split settlements, fees, reversals, chargebacks, weekend/holiday delays, and provider-specific reference IDs, so the simplified matching assumptions could create false matches or false alerts.
2. The current demo lacks production-grade authentication, role-based approvals, tenant isolation, encryption/key management, immutable audit logging, monitoring, and resilient handling of sensitive financial data.
3. Before handling live money data, the system would need provider-specific adapters, currency- and timezone-aware rules, human approval for ambiguous exceptions, secure access controls, tamper-evident audit trails, and extensive reconciliation testing against real bank statements.
