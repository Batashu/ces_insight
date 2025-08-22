from pathlib import Path

def load_sources(src_dir: str):
    """Naively load .txt files as sources; you can extend to pdf/csv/json later."""
    src = Path(src_dir)
    docs = []
    for p in src.rglob('*.txt'):
        try:
            docs.append({'path': str(p), 'text': p.read_text(encoding='utf-8', errors='ignore')})
        except Exception:
            continue
    return docs
