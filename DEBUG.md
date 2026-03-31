# Debugging Resolution

## Issue: Shell Company Detection Failure

- **Cause**: Original implementation used transaction type *counts* (frequencies) in the pattern signature, which meant wallets with the same types but different numbers of transactions got different signatures — even though they were part of the same shell network.
- **Fix**: Simplified to unique transaction type patterns only, ignoring frequency.

## Solution (Applied in `core.py`)

```python
def identify_shell_companies(self):
    clusters = {}
    for wallet, data in self.entity_graph.items():
        if 'transactions' in data.get('metadata', {}):
            transactions = data['metadata']['transactions']
            if transactions:
                # Extract only transaction types (ignore amounts/IDs)
                tx_types = sorted(set(tx.split('_')[0] for tx in transactions))
                pattern = ",".join(tx_types)

                if pattern not in clusters:
                    clusters[pattern] = []
                clusters[pattern].append(wallet)

    # Filter significant clusters (min 3 wallets with same pattern)
    return {k: v for k, v in clusters.items() if len(v) >= 3}
```

## Verification

```bash
$ pytest tests/test_vajra.py -v

tests/test_vajra.py::TestShellCompanyDetection::test_shell_detection PASSED
tests/test_vajra.py::TestShellCompanyDetection::test_no_shells_with_unique_patterns PASSED
tests/test_vajra.py::TestShellCompanyDetection::test_shell_detection_without_transactions PASSED
```

## Common Debugging Tips

### 1. Shell Detection Returns Empty

- Ensure evidence items have `transactions` field in metadata
- Verify minimum 3 wallets share identical type patterns
- Check transaction naming convention uses `type_id` format (e.g., `deposit_1`)

### 2. API Connection Errors

- Validate `BLOCKCHAIN_API_KEY` is set in `.env`
- Check network connectivity
- Review `vajra_errors.log` for structured error details

### 3. Report Generation Issues

- Confirm `case_data` contains both `case_id` and `evidence` keys
- Check that `VajraSystem` doesn't raise `ValueError` on initialization
- Review logger output for processing pipeline errors

### 4. Import Errors

- Ensure `project_vajra/__init__.py` exists
- Run from project root: `python -m project_vajra.core`
- Check virtual environment is activated
