import hashlib, time

def case_id(prefix: str, text: str) -> str:
    h = hashlib.sha1((prefix + '|' + text[:256]).encode('utf-8')).hexdigest()[:10]
    return f"case_{prefix}_{h}"

def simple_id(prefix: str, i: int) -> str:
    return f"{prefix}{i}"
