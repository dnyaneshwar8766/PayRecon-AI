from __future__ import annotations
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

ROUNDING_TOLERANCE = Decimal("0.02")
MAX_NORMAL_SETTLEMENT_DAYS = 2

def money(value: Any) -> Decimal:
    try:
        result = Decimal(str(value)).quantize(Decimal("0.01"))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"Invalid monetary amount: {value!r}")
    if not result.is_finite():
        raise ValueError(f"Invalid monetary amount: {value!r}")
    return result

def parse_date(value: Any) -> date:
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        raise ValueError(f"Date must use YYYY-MM-DD format: {value!r}")

def normalize_platform(rows: list[dict]) -> list[dict]:
    normalized = []
    for i, row in enumerate(rows, 1):
        txid = str(row.get("transaction_id", "")).strip()
        if not txid:
            raise ValueError(f"Platform row {i}: transaction_id is required")
        kind = str(row.get("type", "payment")).strip().lower()
        if kind not in {"payment", "refund"}:
            raise ValueError(f"Platform row {i}: type must be payment or refund")
        normalized.append({
            "transaction_id": txid,
            "customer_id": str(row.get("customer_id", "")).strip(),
            "transaction_date": parse_date(row.get("transaction_date")),
            "amount": money(row.get("amount")),
            "currency": str(row.get("currency", "INR")).strip().upper(),
            "type": kind,
            "original_transaction_id": str(row.get("original_transaction_id", "") or "").strip(),
        })
    return normalized

def normalize_bank(rows: list[dict]) -> list[dict]:
    normalized = []
    for i, row in enumerate(rows, 1):
        entry_id = str(row.get("bank_entry_id", "")).strip() or f"BANK-{i:04d}"
        txid = str(row.get("transaction_id", "")).strip()
        if not txid:
            raise ValueError(f"Bank row {i}: transaction_id is required")
        kind = str(row.get("type", "payment")).strip().lower()
        if kind not in {"payment", "refund"}:
            raise ValueError(f"Bank row {i}: type must be payment or refund")
        normalized.append({
            "bank_entry_id": entry_id,
            "transaction_id": txid,
            "settlement_date": parse_date(row.get("settlement_date")),
            "amount": money(row.get("amount")),
            "currency": str(row.get("currency", "INR")).strip().upper(),
            "type": kind,
            "original_transaction_id": str(row.get("original_transaction_id", "") or "").strip(),
        })
    return normalized

def _issue(code: str, title: str, detail: str, severity: str = "warning") -> dict:
    return {"code": code, "title": title, "detail": detail, "severity": severity}

def reconcile(platform_rows: list[dict], bank_rows: list[dict]) -> dict:
    """Reconcile normalized or raw row dictionaries using deterministic rules."""
    platform = normalize_platform(platform_rows)
    bank = normalize_bank(bank_rows)

    p_by_id: dict[str, list[dict]] = defaultdict(list)
    b_by_id: dict[str, list[dict]] = defaultdict(list)
    for row in platform:
        p_by_id[row["transaction_id"]].append(row)
    for row in bank:
        b_by_id[row["transaction_id"]].append(row)

    # Exact duplicate bank records are marked first, without discarding source rows.
    duplicate_keys = Counter(
        (r["transaction_id"], r["settlement_date"], r["amount"], r["currency"], r["type"])
        for r in bank
    )
    duplicate_ids = {
        r["bank_entry_id"] for r in bank
        if duplicate_keys[(r["transaction_id"], r["settlement_date"], r["amount"], r["currency"], r["type"])] > 1
    }

    results = []
    matched_platform_ids = set()
    used_bank_ids = set()

    for p in platform:
        txid = p["transaction_id"]
        candidates = b_by_id.get(txid, [])
        issues = []
        matching_kind = [b for b in candidates if b["type"] == p["type"]]
        non_duplicate = [b for b in matching_kind if b["bank_entry_id"] not in duplicate_ids]

        if len(p_by_id[txid]) > 1:
            issues.append(_issue("duplicate_platform", "Duplicate platform entry",
                                 "More than one platform row uses this transaction ID.", "critical"))

        if p["type"] == "refund":
            original = p["original_transaction_id"]
            if not original or original not in p_by_id:
                issues.append(_issue("unmatched_refund", "Unmatched refund",
                                     f"Refund {txid} has no original transaction in the platform dataset.", "critical"))

        if not candidates:
            if not issues:
                issues.append(_issue("missing_bank_settlement", "No bank settlement",
                                     "The platform transaction has no bank record in the supplied bank dataset.", "critical"))
            status = "unmatched"
            bank_row = None
        elif len(non_duplicate) == 0 and len(candidates) > 0:
            bank_row = candidates[0]
            if bank_row["bank_entry_id"] in duplicate_ids:
                issues.append(_issue("duplicate_bank", "Duplicate bank entry",
                                     "This bank record is part of an exact duplicate group.", "critical"))
            status = "duplicate"
        elif len(non_duplicate) > 1:
            bank_row = non_duplicate[0]
            issues.append(_issue("ambiguous_match", "Ambiguous bank match",
                                 "Multiple non-duplicate bank entries share this transaction ID; manual review is required.", "critical"))
            status = "review"
        else:
            bank_row = non_duplicate[0]
            used_bank_ids.add(bank_row["bank_entry_id"])
            matched_platform_ids.add(txid)

            if p["currency"] != bank_row["currency"]:
                issues.append(_issue("currency_mismatch", "Currency mismatch",
                                     f"Platform currency {p['currency']} differs from bank currency {bank_row['currency']}.", "critical"))

            diff = abs(p["amount"] - bank_row["amount"])
            if diff > 0:
                if diff <= ROUNDING_TOLERANCE:
                    issues.append(_issue("rounding_difference", "Rounding difference",
                                         f"Amount differs by {diff} {p['currency']}; tolerance is {ROUNDING_TOLERANCE}."))
                else:
                    issues.append(_issue("amount_mismatch", "Amount mismatch",
                                         f"Amount differs by {diff} {p['currency']}.", "critical"))

            if p["type"] == "payment" and bank_row["settlement_date"].month != p["transaction_date"].month:
                if bank_row["settlement_date"] > p["transaction_date"]:
                    issues.append(_issue("late_settlement", "Settled in following month",
                                         f"Transaction date {p['transaction_date']} settled on {bank_row['settlement_date']}."))
            days = (bank_row["settlement_date"] - p["transaction_date"]).days
            if days < 0:
                issues.append(_issue("settlement_before_transaction", "Settlement predates transaction",
                                     "Bank settlement date is earlier than the platform transaction date.", "critical"))
            elif days > MAX_NORMAL_SETTLEMENT_DAYS:
                issues.append(_issue("settlement_delay", "Settlement outside expected window",
                                     f"Settlement took {days} days; assumed normal window is 0–{MAX_NORMAL_SETTLEMENT_DAYS} days."))

            status = "matched" if not issues else ("review" if any(x["severity"] == "critical" for x in issues) else "exception")

        results.append({
            "transaction_id": txid,
            "customer_id": p["customer_id"],
            "transaction_date": p["transaction_date"].isoformat(),
            "platform_amount": str(p["amount"]),
            "bank_amount": str(bank_row["amount"]) if bank_row else None,
            "currency": p["currency"],
            "bank_settlement_date": bank_row["settlement_date"].isoformat() if bank_row else None,
            "type": p["type"],
            "status": status,
            "issues": issues,
        })

    # Bank entries with no platform counterpart, including orphaned refunds.
    for b in bank:
        if b["transaction_id"] not in p_by_id:
            code = "unmatched_refund" if b["type"] == "refund" else "bank_only_entry"
            title = "Unmatched refund" if code == "unmatched_refund" else "Bank-only entry"
            detail = (f"Refund references original transaction {b['original_transaction_id'] or 'not supplied'}, "
                      "but no matching original platform transaction exists.") if code == "unmatched_refund" else \
                     "A bank entry exists without a corresponding platform transaction."
            results.append({
                "transaction_id": b["transaction_id"], "customer_id": "",
                "transaction_date": None, "platform_amount": None,
                "bank_amount": str(b["amount"]), "currency": b["currency"],
                "bank_settlement_date": b["settlement_date"].isoformat(),
                "type": b["type"], "status": "review",
                "issues": [_issue(code, title, detail, "critical")],
            })

    counts = Counter(r["status"] for r in results)
    issue_counts = Counter(issue["code"] for row in results for issue in row["issues"])
    platform_total = sum((r["amount"] for r in platform if r["type"] == "payment"), Decimal("0.00"))
    bank_total = sum((r["amount"] for r in bank if r["type"] == "payment"), Decimal("0.00"))

    return {
        "summary": {
            "platform_transactions": len(platform),
            "bank_entries": len(bank),
            "matched": counts.get("matched", 0),
            "exceptions": counts.get("exception", 0),
            "unmatched": counts.get("unmatched", 0),
            "needs_review": counts.get("review", 0) + counts.get("duplicate", 0),
            "platform_payment_total": str(platform_total),
            "bank_payment_total": str(bank_total),
            "net_difference": str((platform_total - bank_total).quantize(Decimal("0.01"))),
            "discrepancy_count": sum(issue_counts.values()),
        },
        "issue_counts": dict(issue_counts),
        "results": results,
        "assumptions": [
            "Transaction ID is the primary matching key.",
            "Expected normal settlement window is 0–2 calendar days.",
            "Rounding tolerance is 0.02 currency units.",
            "A payment settling in a later calendar month is flagged as late settlement.",
            "Duplicate bank rows are identified by transaction ID, settlement date, amount, currency and type.",
            "Ambiguous matches are sent for review; the engine does not silently choose a winner."
        ]
    }
