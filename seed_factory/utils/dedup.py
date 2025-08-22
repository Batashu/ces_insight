from pathlib import Path
import hashlib, json

def deduplicate(docs, out_dir: str):
    outp = Path(out_dir)
    outp.mkdir(parents=True, exist_ok=True)
    seen = set()
    kept = 0
    for d in docs:
        h = hashlib.sha1(d['text'].encode('utf-8')).hexdigest()
        if h in seen: 
            continue
        seen.add(h)
        kept += 1
        (outp / f'source_{kept:05d}.txt').write_text(d['text'], encoding='utf-8')
    return kept
