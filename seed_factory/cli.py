import argparse, json, os
from pathlib import Path

from .ingest.readers import load_sources
from .ingest.license_filter import allow_licensed
from .ingest.pii_masker import redact_pii
from .utils.dedup import deduplicate

from .draft.fact_extract import facts_from_text
from .draft.hypothesis_summarize import summarize_hypothesis
from .draft.test_gen import gen_tests_from_facts
from .draft.result_extract import results_from_text
from .draft.causal_builder import build_causal_map
from .draft.contra_detect import find_contradictions

from .gold.schema_reduce import minimal_schema_from_draft
from .gold.closure_decide import closure_from_coverage

from .verify.rule_executor import simulate
from .verify.validator import validate_dir

def cmd_ingest(args):
    docs = load_sources(args.src)
    docs = allow_licensed(docs, args.allow_licenses.split(','))
    docs = redact_pii(docs)
    kept = deduplicate(docs, args.out)
    print(f"Ingested {len(docs)} docs, kept {kept} unique -> {args.out}")

def _draft_one(text: str, source_name: str, idx: int):
    facts_text = facts_from_text(text)
    facts = [{"id": f"F{i+1}", "text": t, "spans": [{"source_id": source_name, "start": 0, "end": min(100,len(text))}]} for i,t in enumerate(facts_text)]
    hyp = summarize_hypothesis(facts_text)
    tests = gen_tests_from_facts(facts_text)
    results = results_from_text(text)
    causal = build_causal_map(facts_text)
    schema = minimal_schema_from_draft(causal)
    cov = simulate(schema.get('rules',[]), tests)
    closure = closure_from_coverage(cov['coverage'])
    case = {
        "id": f"case_auto_{idx:05d}",
        "domain": "physics",   # default; adjust later via glossary/tagging
        "meta": {"source": source_name},
        "facts": facts,
        "hypothesis": hyp,
        "tests": tests,
        "results": results,
        "causal_map": causal,
        "gestalt": {"coherence":"", "dissonance":"", "ambiguity":""},
        "gold_schema": schema,
        "closure_gold": closure,
        "contra_pairs": find_contradictions(facts_text)
    }
    return case

def cmd_draft(args):
    outp = Path(args.out); outp.mkdir(parents=True, exist_ok=True)
    files = sorted(Path(args.in_).glob('*.txt'))
    n = 0
    for i, f in enumerate(files, 1):
        text = f.read_text(encoding='utf-8', errors='ignore')
        case = _draft_one(text, f.name, i)
        (outp / f"{case['id']}.json").write_text(json.dumps(case, ensure_ascii=False, indent=2), encoding='utf-8')
        n += 1
    print(f"Drafted {n} cases -> {args.out}")

def cmd_review(args):
    # Minimal: copy draft -> gold (you can open/edit manually before copying)
    inp = Path(args.in_); outp = Path(args.out); outp.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(inp.glob('*.json')):
        data = json.loads(f.read_text(encoding='utf-8'))
        # run quick sim for info (no gate)
        cov = simulate(data.get('gold_schema',{}).get('rules',[]), data.get('tests',[]))
        data.setdefault('meta',{})['coverage_preview'] = cov['coverage']
        (outp/f.name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        n += 1
    print(f"Reviewed (copied) {n} cases -> {args.out}")

def cmd_validate(args):
    report = validate_dir(args.in_)
    bad = [k for k,v in report.items() if not v['ok']]
    print(json.dumps(report, indent=2))
    if bad:
        print(f"\n{len(bad)} files with issues: {bad}")
    else:
        print("All cases passed basic validation.")

def cmd_split(args):
    from .split.composer import make_splits
    stats = make_splits(args.in_, args.out)
    print(f"Splits -> {args.out} :: {stats}")

def main():
    ap = argparse.ArgumentParser("Seed Case Factory CLI")
    sub = ap.add_subparsers(dest='cmd', required=True)

    ap_i = sub.add_parser('ingest', help='Ingest sources -> data/raw')
    ap_i.add_argument('--src', required=True)
    ap_i.add_argument('--out', required=True)
    ap_i.add_argument('--allow-licenses', default='CC-BY,CC0,MIT')
    ap_i.set_defaults(func=cmd_ingest)

    ap_d = sub.add_parser('draft', help='Build naive draft cases from data/raw')
    ap_d.add_argument('--in', dest='in_', required=True)
    ap_d.add_argument('--out', required=True)
    ap_d.set_defaults(func=cmd_draft)

    ap_r = sub.add_parser('review', help='Copy drafts -> gold with quick coverage preview')
    ap_r.add_argument('--in', dest='in_', required=True)
    ap_r.add_argument('--out', required=True)
    ap_r.set_defaults(func=cmd_review)

    ap_v = sub.add_parser('validate', help='Validate gold cases')
    ap_v.add_argument('--in', dest='in_', required=True)
    ap_v.set_defaults(func=cmd_validate)

    ap_s = sub.add_parser('split', help='Create splits from gold')
    ap_s.add_argument('--in', dest='in_', required=True)
    ap_s.add_argument('--out', required=True)
    ap_s.set_defaults(func=cmd_split)

    args = ap.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
