import re

DEF_RE = re.compile(r'(\b[\w\-]+\b)\s+is\s+(?:defined\s+as|the)\s+(.*?)[\.\n]')
CAUSE_RE = re.compile(r'(increase[s]? in|higher|more)\s+(\b[\w\-]+\b).*?(increase[s]?|decrease[s]?|reduce[s]?|lower)\s+(\b[\w\-]+\b)', re.I)

def extract_facts(text: str):
    facts = []
    for m in DEF_RE.finditer(text):
        term, defin = m.group(1), m.group(2)
        facts.append(f\"{term} is {defin.strip()}.\")
    for m in CAUSE_RE.finditer(text):
        facts.append(f\"{m.group(2)} {m.group(1)} -> {m.group(4)} {m.group(3)}.\")
    return list(dict.fromkeys(facts))[:10]  # unique + cap
