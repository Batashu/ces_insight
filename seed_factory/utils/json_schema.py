from dataclasses import dataclass, field, asdict
from typing import List, Dict, Literal, Optional

Relation = Literal["increase","decrease","enable","prevent","cause","modulate","equal","greater_than","less_than"]

@dataclass
class Fact:
    id: str
    text: str
    spans: List[Dict] = field(default_factory=list)  # [{source_id,start,end}]

@dataclass
class Test:
    id: str
    do: str
    expect: str
    units: Dict[str, str] = field(default_factory=dict)

@dataclass
class Result:
    id: str
    obs: str
    value: Optional[float] = None
    unit: Optional[str] = None
    spans: List[Dict] = field(default_factory=list)

@dataclass
class Edge:
    frm: str  # 'from'
    to: str
    type: Relation
    sign: Literal['+','-','0'] = "+"

@dataclass
class CausalMap:
    nodes: List[str]
    edges: List[Edge]

@dataclass
class GoldRule:
    if_: List[str]    # key name 'if_' to avoid Python keyword; JSON key will be 'if'
    then: List[str]
    citations: List[str]

@dataclass
class GoldSchema:
    schema_id: str
    vars: List[str]
    rules: List[GoldRule]
    assumptions: List[str] = field(default_factory=list)
    scope: str = ""

@dataclass
class Case:
    id: str
    domain: str
    meta: Dict = field(default_factory=dict)
    facts: List[Fact] = field(default_factory=list)
    hypothesis: str = ""
    tests: List[Test] = field(default_factory=list)
    results: List[Result] = field(default_factory=list)
    causal_map: CausalMap = None
    gestalt: Dict = field(default_factory=lambda: {"coherence":"","dissonance":"","ambiguity":""})
    gold_schema: GoldSchema = None
    closure_gold: Literal['PASS','FAIL'] = "FAIL"
    contra_pairs: List[List[str]] = field(default_factory=list)

def to_json_dict(case: Case) -> Dict:
    # Convert dataclasses to JSON-friendly dict and map if_ -> 'if'
    def map_rule(rule: GoldRule) -> Dict:
        return {"if": rule.if_, "then": rule.then, "citations": rule.citations}
    d = asdict(case)
    # fix edges key 'frm' -> 'from', and rules key 'if_' -> 'if'
    if 'causal_map' in d and d['causal_map']:
        for e in d['causal_map'].get('edges', []):
            e['from'] = e.pop('frm', None)
    if d.get('gold_schema'):
        d['gold_schema']['rules'] = [map_rule(r) for r in case.gold_schema.rules]
    return d
