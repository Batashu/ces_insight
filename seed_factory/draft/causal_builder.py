def build_causal_map(facts):
    nodes = set()
    edges = []
    for f in facts:
        if '->' in f:
            lhs, rhs = [x.strip() for x in f.split('->', 1)]
            a = lhs.split()[0]
            b = rhs.split()[0]
            nodes.add(a); nodes.add(b)
            edges.append({'from': a, 'to': b, 'type': 'increase', 'sign': '+'})
    return {'nodes': sorted(list(nodes)), 'edges': edges}
