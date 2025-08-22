import re

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
PHONE_RE = re.compile(r'(\+?\d[\d\-\s]{7,}\d)')
KEYLIKE_RE = re.compile(r'(?i)(api[_\- ]?key|secret|token)[=:]\s*([A-Za-z0-9\-\._]{10,})')

def redact_pii(docs):
    out = []
    for d in docs:
        t = d['text']
        t = EMAIL_RE.sub('[REDACTED_EMAIL]', t)
        t = PHONE_RE.sub('[REDACTED_PHONE]', t)
        t = KEYLIKE_RE.sub('[REDACTED_KEY]', t)
        out.append({**d, 'text': t})
    return out
