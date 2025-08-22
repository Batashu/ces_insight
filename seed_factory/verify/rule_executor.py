# verify/rule_executor.py (sketch)
def simulate(schema_rules, tests):
    """
    Evaluate schema rules against tests -> predicted outcomes,
    compare with expected 'expect' fields -> coverage fraction.
    Relations supported: increase/decrease/enable/prevent/cause/modulate/equal/gt/lt
    """
    # 1) Parse rules into state deltas over vars
    # 2) Apply do() interventions -> propagate via edges
    # 3) Compare predicted qualitative signs vs test.expect
    return {"coverage": 0.0..1.0, "mismatches":[...]}
