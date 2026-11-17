from datetime import date
from .engine import reconcile

def sample_rows():
    platform = [
        {"transaction_id":"TXN-1001","customer_id":"CUS-201","transaction_date":"2026-10-28","amount":"1250.00","currency":"INR","type":"payment"},
        {"transaction_id":"TXN-1002","customer_id":"CUS-202","transaction_date":"2026-10-31","amount":"899.00","currency":"INR","type":"payment"},
        {"transaction_id":"TXN-1003","customer_id":"CUS-203","transaction_date":"2026-10-29","amount":"450.50","currency":"INR","type":"payment"},
        {"transaction_id":"TXN-1004","customer_id":"CUS-204","transaction_date":"2026-10-30","amount":"700.00","currency":"INR","type":"payment"},
        {"transaction_id":"TXN-1005","customer_id":"CUS-205","transaction_date":"2026-10-30","amount":"320.00","currency":"INR","type":"payment"},
        {"transaction_id":"TXN-1006","customer_id":"CUS-206","transaction_date":"2026-10-30","amount":"150.00","currency":"INR","type":"payment"},
        {"transaction_id":"TXN-1007","customer_id":"CUS-207","transaction_date":"2026-10-30","amount":"210.00","currency":"INR","type":"payment"},
        {"transaction_id":"REF-2001","customer_id":"CUS-208","transaction_date":"2026-10-31","amount":"-75.00","currency":"INR","type":"refund","original_transaction_id":"TXN-MISSING-77"},
    ]
    bank = [
        {"bank_entry_id":"BNK-5001","transaction_id":"TXN-1001","settlement_date":"2026-10-29","amount":"1250.00","currency":"INR","type":"payment"},
        {"bank_entry_id":"BNK-5002","transaction_id":"TXN-1002","settlement_date":"2026-11-01","amount":"899.00","currency":"INR","type":"payment"},
        {"bank_entry_id":"BNK-5003","transaction_id":"TXN-1003","settlement_date":"2026-10-30","amount":"450.49","currency":"INR","type":"payment"},
        {"bank_entry_id":"BNK-5004","transaction_id":"TXN-1004","settlement_date":"2026-10-31","amount":"700.00","currency":"INR","type":"payment"},
        {"bank_entry_id":"BNK-5005","transaction_id":"TXN-1004","settlement_date":"2026-10-31","amount":"700.00","currency":"INR","type":"payment"},
        {"bank_entry_id":"BNK-5006","transaction_id":"TXN-1005","settlement_date":"2026-11-02","amount":"320.00","currency":"INR","type":"payment"},
        {"bank_entry_id":"BNK-5007","transaction_id":"TXN-1006","settlement_date":"2026-10-31","amount":"150.00","currency":"INR","type":"payment"},
        {"bank_entry_id":"BNK-5010","transaction_id":"TXN-1007","settlement_date":"2026-10-31","amount":"209.98","currency":"INR","type":"payment"},
        {"bank_entry_id":"BNK-5008","transaction_id":"REF-2001","settlement_date":"2026-11-01","amount":"-75.00","currency":"INR","type":"refund","original_transaction_id":"TXN-MISSING-77"},
        {"bank_entry_id":"BNK-5009","transaction_id":"TXN-BANK-ONLY","settlement_date":"2026-11-01","amount":"88.00","currency":"INR","type":"payment"},
    ]
    return {"platform": platform, "bank": bank}
