ces_insight/
  seed_factory/
    __init__.py
    cli.py                     # Typer/Click CLI
    ingest/
      readers.py               # pdf/txt/json/csv/jsonl readers
      license_filter.py        # license classifier + allowlist
      pii_masker.py            # phones/emails/API keys
    draft/
      glossary_index.py        # entity/unit lexicons; cosine sim
      fact_extract.py          # F1..Fn extraction (rules+SLM-A)
      hypothesis_summarize.py  # 1–2 sentence central claim
      test_gen.py              # do() tests from text or templates
      result_extract.py        # R1..Rm from text (numbers/units)
      causal_builder.py        # nodes/edges from claims
      contra_detect.py         # contradiction pairs from corpus
      heuristics.py            # regex patterns for relations
    gold/
      annotate.py              # human-in-the-loop curation helpers
      schema_reduce.py         # MDL-style minimal schema
      closure_decide.py        # PASS/FAIL decision rule
    verify/
      truth_contract.yml       # domain rules (sources/recency/units)
      unit_normalizer.py       # pint-backed unit normalization
      span_aligner.py          # citation span ↔ answer tokens
      rule_executor.py         # closed-ontology simulator
      validator.py             # end-to-end case checks
      fixtures/                # 30+ regression fixtures
    split/
      composer.py              # OOD composition splits
    utils/
      ids.py                   # case/F*/T*/R* id allocators
      dedup.py                 # MinHash/SimHash dedup
      json_schema.py           # pydantic models + JSON schema
  data/
    raw/                       # ingested sources (sanitized)
    draft/                     # auto drafts (need review)
    gold/                      # finalized cases
    splits/                    # train/dev/test indices
