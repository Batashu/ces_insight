# seed_factory/utils/json_schema.py
from pydantic import BaseModel, Field, validator
from typing import List, Literal, Dict

Relation = Literal["increase","decrease","enable","prevent","cause","modulate","equal","greater_than","less_than"]

class Fact(BaseModel):
    id: str
    text: str
    spans: List[Dict] = []         # [{"source_id": "...", "start": 120, "end": 145}]

class Test(BaseModel):
    id: str
    do: str                         # interventional statement
    expect: str                     # expected qualitative/quantitative outcome
    units: Dict[str, str] = {}      # {"V": "volt", "I": "ampere"}

class Result(BaseModel):
    id: str
    obs: str
    value: float | None = None
    unit: str | None = None
    spans: List[Dict] = []

class Edge(BaseModel):
    frm: str = Field(..., alias="from")
    to: str
    type: Relation
    sign: Literal["+", "-", "0"] = "+"

class CausalMap(BaseModel):
    nodes: List[str]
    edges: List[Edge]

class GoldRule(BaseModel):
    if_: List[str] = Field(..., alias="if")   # e.g., ["V increase", "R constant"]
    then: List[str]                           # e.g., ["I increase"]
    citations: List[str]                      # refs like "F1","T2","R3"

class GoldSchema(BaseModel):
    schema_id: str
    vars: List[str]
    rules: List[GoldRule]
    assumptions: List[str] = []
    scope: str = ""

class Case(BaseModel):
    id: str
    domain: str
    meta: Dict = {}
    facts: List[Fact]
    hypothesis: str
    tests: List[Test]
    results: List[Result]
    causal_map: CausalMap
    gestalt: Dict = {"coherence": "", "dissonance": "", "ambiguity": ""}
    gold_schema: GoldSchema
    closure_gold: Literal["PASS","FAIL"]
    contra_pairs: List[List[str]] = []   # [["claim_a","claim_b","contradict"]]
