# Test plan

| ID | Scenario | Expected result |
|---|---|---|
| TC-01 | Exact ID, currency and amount match | `matched` |
| TC-02 | Platform transaction 31 Oct, bank settlement 1 Nov | `late_settlement` |
| TC-03 | Difference of 0.01 | `rounding_difference` |
| TC-04 | Exact duplicate bank record | `duplicate_bank` |
| TC-05 | Refund points to missing original transaction | `unmatched_refund` |
| TC-06 | Difference greater than 0.02 | `amount_mismatch` |
| TC-07 | More than one bank candidate | `ambiguous_match` |
| TC-08 | Invalid date or amount | HTTP 422 / ValueError |
| TC-09 | Bank-only payment | `bank_only_entry` |
| TC-10 | Currency differs | `currency_mismatch` |

Run the executable tests with `py -m pytest -q` from the backend directory.


## Execution status
The backend suite was run in the build environment and passed 8 tests. Keep a screenshot or terminal capture from your own local run as assessment evidence. Frontend build verification remains outstanding because dependency installation timed out in the build environment.
