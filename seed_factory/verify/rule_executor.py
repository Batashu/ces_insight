def simulate(schema_rules, tests):
    # naive coverage: if any test's 'expect' contains 'increase' and any rule has 'then' with 'increase', count as covered
    if not tests or not schema_rules:
        return {'coverage': 0.0, 'mismatches': []}
    covered = 0
    for t in tests:
        exp = t.get('expect','')
        hit = any('increase' in exp and any('increase' in x for x in r.get('then', [])) for r in schema_rules)
        if hit:
            covered += 1
    return {'coverage': covered/len(tests), 'mismatches': []}
