import json, hashlib
from pathlib import Path

def make_splits(in_dir: str, out_dir: str):
    inp = Path(in_dir); outp = Path(out_dir); outp.mkdir(parents=True, exist_ok=True)
    files = sorted([p for p in inp.glob('*.json')])
    train, dev, test = [], [], []
    for f in files:
        h = int(hashlib.sha1(f.name.encode('utf-8')).hexdigest(), 16)
        r = h % 100
        if r < 70: train.append(f.name)
        elif r < 85: dev.append(f.name)
        else: test.append(f.name)
    (outp/'train.txt').write_text('\n'.join(train), encoding='utf-8')
    (outp/'dev.txt').write_text('\n'.join(dev), encoding='utf-8')
    (outp/'test.txt').write_text('\n'.join(test), encoding='utf-8')
    return {'train': len(train), 'dev': len(dev), 'test': len(test)}
