import json
from pathlib import Path
from .rule_executor import simulate
from .span_aligner import span_match_ok
from .unit_normalizer import normalize_units

REQUIRED_KEYS = ['id','domain','facts','hypothesis','tests','results','causal_map','gold_schema','closure_gold']

def validate_case_file(path: str) -> dict:
    d = json.loads(Path(path).read_text(encoding='utf-8'))
    ok, msgs = True, []
    for k in REQUIRED_KEYS:
        if k not in d:
            ok = False; msgs.append(f'missing key: {k}')
    # span match
    span_ok, pct = span_match_ok(d, 95)
    if not span_ok:
        ok = False; msgs.append(f'span match failed: {pct:.1f}%')
    # coverage
    schema_rules = d.get('gold_schema',{}).get('rules',[])
    cov = simulate(schema_rules, d.get('tests',[]))
    if cov['coverage'] < 0.2:
        msgs.append(f'low coverage: {cov["coverage"]:.2f}')
    return {'ok': ok, 'msgs': msgs, 'coverage': cov['coverage']}

def validate_dir(dir_in: str) -> dict:
    p = Path(dir_in)
    reports = {}
    for f in p.glob('*.json'):
        reports[f.name] = validate_case_file(str(f))
    return reports
