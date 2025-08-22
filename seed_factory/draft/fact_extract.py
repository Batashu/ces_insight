from .heuristics import extract_facts

def facts_from_text(text: str):
    return extract_facts(text)
