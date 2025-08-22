def gen_tests_from_facts(facts):
    tests = []
    i = 1
    for f in facts:
        if '->' in f:
            lhs, rhs = [x.strip() for x in f.split('->', 1)]
            tests.append({'id': f'T{i}', 'do': f'increase {lhs}', 'expect': rhs.split()[0] + ' ' + rhs.split()[1]})
            i += 1
            if i > 3: break
    if not tests:
        tests.append({'id': 'T1', 'do': 'no_op', 'expect': 'no_change'})
    return tests
