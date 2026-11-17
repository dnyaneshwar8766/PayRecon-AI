from app.engine import reconcile
from app.sample_data import sample_rows
from decimal import Decimal

def test_all_four_required_scenarios_are_detected():
    data = sample_rows()
    result = reconcile(data["platform"], data["bank"])
    codes = {issue["code"] for row in result["results"] for issue in row["issues"]}
    assert "late_settlement" in codes
    assert "rounding_difference" in codes
    assert "duplicate_bank" in codes
    assert "unmatched_refund" in codes

def test_exact_match_is_matched():
    p = [{"transaction_id":"A1","transaction_date":"2026-01-01","amount":"100.00","currency":"INR","type":"payment"}]
    b = [{"bank_entry_id":"B1","transaction_id":"A1","settlement_date":"2026-01-02","amount":"100.00","currency":"INR","type":"payment"}]
    result = reconcile(p, b)
    assert result["results"][0]["status"] == "matched"
    assert result["summary"]["matched"] == 1

def test_rounding_tolerance():
    p = [{"transaction_id":"A1","transaction_date":"2026-01-01","amount":"100.00","currency":"INR","type":"payment"}]
    b = [{"bank_entry_id":"B1","transaction_id":"A1","settlement_date":"2026-01-01","amount":"99.99","currency":"INR","type":"payment"}]
    result = reconcile(p, b)
    assert "rounding_difference" in {i["code"] for i in result["results"][0]["issues"]}

def test_large_amount_difference_is_critical():
    p = [{"transaction_id":"A1","transaction_date":"2026-01-01","amount":"100.00","currency":"INR","type":"payment"}]
    b = [{"bank_entry_id":"B1","transaction_id":"A1","settlement_date":"2026-01-01","amount":"90.00","currency":"INR","type":"payment"}]
    result = reconcile(p, b)
    assert "amount_mismatch" in {i["code"] for i in result["results"][0]["issues"]}

def test_invalid_date_is_rejected():
    p = [{"transaction_id":"A1","transaction_date":"not-a-date","amount":"100","type":"payment"}]
    try:
        reconcile(p, [])
        assert False, "Expected validation error"
    except ValueError:
        assert True

def test_orphan_bank_refund_is_flagged():
    p = []
    b = [{"bank_entry_id":"B1","transaction_id":"R1","settlement_date":"2026-02-01","amount":"-20","type":"refund","original_transaction_id":"OLD1"}]
    result = reconcile(p, b)
    assert "unmatched_refund" in {i["code"] for r in result["results"] for i in r["issues"]}

def test_reconciliation_run_is_persisted_and_retrievable():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    sample = client.get('/api/sample').json()
    response = client.post('/api/reconcile', json=sample)
    assert response.status_code == 200
    run_id = response.json()['run']['id']
    history = client.get('/api/runs').json()['runs']
    assert any(item['id'] == run_id for item in history)
    detail = client.get(f'/api/runs/{run_id}')
    assert detail.status_code == 200
    assert detail.json()['summary'] == response.json()['summary']


def test_sample_rounding_drift_accumulates_across_transactions():
    data = sample_rows()
    result = reconcile(data["platform"], data["bank"])
    platform_by_id = {r["transaction_id"]: r for r in data["platform"]}
    bank_by_id = {r["transaction_id"]: r for r in data["bank"]}
    deltas = [abs(Decimal(platform_by_id[tx]["amount"]) - Decimal(bank_by_id[tx]["amount"]))
              for tx in ("TXN-1003", "TXN-1007")]
    assert all(Decimal("0") < delta <= Decimal("0.02") for delta in deltas)
    assert sum(deltas) == Decimal("0.03")
    assert "rounding_difference" in result["issue_counts"]
