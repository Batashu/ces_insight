def minimal_schema_from_draft(causal_map):
    rules = []
    for e in causal_map.get('edges', [])[:1]:  # take first edge only (MDL-ish)
        rules.append({'if': [f"{e['from']} increase"], 'then': [f"{e['to']} increase"], 'citations': ['F1']})
    vars_ = causal_map.get('nodes', [])
    return {'schema_id': 'AUTO_MIN_1', 'vars': vars_, 'rules': rules, 'assumptions': [], 'scope': ''}
