def summarize_hypothesis(facts):
    if not facts:
        return ""
    # naive: use first causal-looking fact as hypothesis, else first fact
    for f in facts:
        if '->' in f:
            return f"If {f.split('->')[0].strip()}, then {f.split('->')[1].strip()}"
    return facts[0][:160]
