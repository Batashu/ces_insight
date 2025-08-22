# seed_factory/cli.py
import typer
from ingest.readers import load_sources
from ingest.license_filter import allow_licensed
from ingest.pii_masker import redact_pii
from utils.dedup import deduplicate
from draft import fact_extract, hypothesis_summarize, test_gen, result_extract, causal_builder, contra_detect
from verify.validator import validate_case
from split.composer import make_splits

app = typer.Typer()

@app.command()
def ingest(src: str, out: str, allow_licenses: str = "CC-BY,CC0,MIT"):
    docs = load_sources(src)
    docs = allow_licensed(docs, allow_licenses.split(","))
    docs = redact_pii(docs)
    deduplicate(docs, out)

@app.command()
def draft(in_: str, out: str):
    # iterate docs -> auto-draft cases
    ...

@app.command()
def review(bundle: str, edit: bool = True):
    # open cases one-by-one, run live verify, write to data/gold
    ...

@app.command()
def validate(in_: str, fixtures: str | None = None):
    # run truth contract, span align, rule executor, schema checks
    ...

@app.command()
def split(in_: str, out: str, ood_combo: bool = True):
    make_splits(in_, out, ood_combo)

if __name__ == "__main__":
    app()
