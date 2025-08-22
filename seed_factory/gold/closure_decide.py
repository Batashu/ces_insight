def closure_from_coverage(coverage: float) -> str:
    return 'PASS' if coverage >= 0.6 else 'FAIL'
