Got it. Below is a **rewritten roadmap** that preserves your structure but integrates my ruthless-review insights. I’ve kept the original numbering but adjusted emphasis, pacing, and sequencing to reflect reality: verifiers and seed cases first, adapters gradual, timeline open-ended.

---

# Insight-First LLM Roadmap (Phi-4 4-bit)

**Owner:** Tuhin Gupta, MD
**Objective:** Build an insight-capable system under strict compute (4-bit Phi-4 ceiling) using behavioral reward shaping, curriculum compression, modular adapters, and structured data.
**Guardrail:** Truth > Coherence > Novelty. No uncontrolled hallucinations.

---

## 0) Constraints & Targets

* **Hardware:** RTX 5080, 32GB RAM; 4-bit quant Phi-4 as ceiling; optional 1–3B SLMs (quantized) for control stages.
* **Latency budget:** < 2.5 s end-to-end for typical QA; < 7 s with retrieval.
* **Primary outputs:**

  1. Minimal schemas (machine-checkable)
  2. Causal answers to `do()` queries
  3. Closure decisions with justification

**Acceptance (global):**

* Hallucination rate < 1% on fact-checked sets
* Closure accuracy ≥ 90% on held-out contradictions
* Schema coverage ≥ 85% with Length Ratio ≤ 0.6 vs baseline

---

## 1) System Architecture (high-level)

**Pipeline:**

1. **SLM-A (Distiller/Parser, 1–3B):** Normalize query → extract entities/units → cast into *Fact → Hypothesis → Test → Interpretation → Generalization* + candidate stubs.
2. **SLM-B (Retriever/Rationalizer, 1–3B):** Retrieve (BM25 + embeddings), dedupe, rank chunks; mark contradictions; propose candidate schemas + assumptions + predictions.
3. **Reasoner (Phi-4 4-bit):** With adapters + auxiliary heads, produce **compact schema**, **causal answers**, **closure verdict**, **citations**.
4. **Verifiers (deterministic tools):** Evidence aligner, contradiction detector, unit/logic validator, rule executor.
5. **Memory:** Schema Archive (canonical JSON), Causal Graph Store, Gestalt Logs.

**Data flow:** Text → Structured Record → Evidence Pack → Reasoner → Schema JSON + Answers → Verifier → Persist.

---

## 2) Data & Curriculum

### 2.1 Canonical JSONL

```json
{
  "id": "case_0001",
  "domain": "physics",
  "facts": [ {"id":"F1","text":"…"} ],
  "hypothesis": "…",
  "tests": [ {"id":"T1","do":"…","expect":"…"} ],
  "results": [ {"id":"R1","obs":"…"} ],
  "causal_map": {
    "nodes": ["A","B","C"],
    "edges": [{"from":"A","to":"B","type":"causes","sign":"+"}]
  },
  "gestalt": {"coherence":"…","dissonance":"…","ambiguity":"…"},
  "gold_schema": {
    "schema_id":"…",
    "vars":["…"],
    "rules":[{"if":["…"],"then":["…"]}],
    "assumptions":["…"],
    "scope":"…",
    "citations":["F1","T1"]
  },
  "closure_gold": "PASS",
  "contra_pairs": [["claim_a","claim_b","label"]]
}
```

### 2.2 Curriculum Ladder

* **Stage A: Primitives → glossaries** (definitions, units, entity linking).
* **Stage B: K-12 → Undergrad → Grad** (progressive abstraction, problem sets).
* **Stage C: Research-style** (Fact→Hyp→Test→Interp→Gen with gold schemas).
* **Stage D: Cross-domain transfer** (math → language → psychology → ethics → programming → back to math).

**Splits:** 70/15/15 with OOD compositions.
**Quality gates:** license filter, dedup, unit normalization, reference IDs.

---

## 3) Reward & Punishment Hierarchy

**Loss components:**

* **L\_schema:** schema JSON generation (EM, MDL penalty).
* **L\_cov:** schema vs test/results coverage.
* **L\_cite:** every rule must cite evidence.
* **L\_causal:** answer interventional `do()` queries.
* **L\_close:** closure verdict classifier.
* **L\_contra:** contradiction pair classifier.
* **L\_hallucination:** penalty if verifier flags unsupported.
* **L\_overconfidence:** penalty for certainty without evidence.

**Total loss:**

$$
L = L_{LM} + \lambda_s L_{schema} + \lambda_{cov} L_{cov} + \lambda_{cite} L_{cite} + \lambda_{caus} L_{causal} + \lambda_{close} L_{close} + \lambda_{contra} L_{contra} + \lambda_h L_{hallucination} + \lambda_o L_{overconfidence}
$$

**Decode constraints:** JSON grammar, closed ontology, beam re-rank by (coverage − length).

---

## 4) Execution Order (revised)

**Foundational before training:**

1. **Seed Case Factory**

   * Goal: 5k–10k high-quality JSONL cases across at least 2 domains (physics, psychology/ethics).
   * Method: semi-automatic extraction from textbooks + manual curation.

2. **Verifier Suite**

   * Truth contract (sources, recency, numeric tolerance, units).
   * Rule executor (closed ontology).
   * Citation span-aligner.
   * Unit normalizer.
   * Regression tests on 30 fixtures.

**Only once these are stable:**

* Train schema adapter head.
* Add causal QA.
* Add closure/contradiction heads.
* Add novelty reward last.

Adapters: start with one (schema). Add others only if metrics plateau.

---

## 5) Small-Model Cascade

* **SLM-A:** parsing into entities, units, stubs.
* **SLM-B:** retrieval + contradiction marking.
* **Benefit:** lowers entropy + token count before Phi-4, keeps latency budget.

Router decides cascade vs adapter direct vs hybrid (see §11).

---

## 6) Evaluation Suite

* **Schema EM / F1 (length-penalized)**
* **Coverage score** (entailed tests/results)
* **Causal EM** (do() + counterfactuals)
* **Closure accuracy**
* **Contradiction rate**
* **Hallucination rate / Overconfidence calibration**
* **Novelty precision/recall**
* **Latency & token-efficiency**

KPIs logged to dashboard; rollback on regression.

---

## 7) Repo & Ops

```
ces_insight/
  data/
    raw/ processed/
  schemas/
  verifiers/
  adapters/
  trainers/
  eval/
  tools/
  docs/
```

* **Versioning:** DVC for data; W\&B or local logs for runs.
* **Checkpoints:** keyed to Schema F1 and Causal EM.
* **Decoding:** JSON FSM + retries.
* **Rollback:** automatic on KPI regression.

---

## 8) Risks & Mitigations

* **Seed data bottleneck:** build factory pipeline first.
* **Verifier fragility:** treat as compiler; regression tests mandatory.
* **Adapter interference:** one adapter first, then expand.
* **Calibration drift:** monitor ECE, Brier; retrain Dirichlet head if off.
* **Novelty bias:** reward only if coverage passes.
* **Ops overload:** automate pins, hashes, and env setup.

---

## 9) Perception Layer Routing

**Signals:**

* **Semantic/factual triggers:** define, date, who, when, where, cite, latest, summarize, evidence.
* **Reasoning triggers:** why, what-if, schema, causal, contradiction, interpret, design.
* **Uncertainty:** entropy, Dirichlet α.
* **Evidence need:** numbers, time-sensitive domains.

**Policy:**

* Route to **cascade** if semantic/time-sensitive/low similarity/high entropy.
* Route to **adapters** if purely reasoning.
* **Hybrid** if mixed/ambiguous.
* **Fallback:** always cascade if verifiers flag unsupported numbers, contradictions, or low confidence.

---

## 10) Risk Mitigation Modules

* **Truth Contract:** explicit source + recency rules.
* **Coverage Engine:** deterministic ontology executor.
* **Calibration & Overconfidence:** Dirichlet head + temp scaling.
* **Adversarial Curriculum:** near-miss schemas, spurious correlation traps, counterfactual negatives.
* **Retrieval ROI:** stop retrieval when marginal coverage gain < threshold.
* **Privacy & Licensing:** license filter + PII masker.
* **Ops & Repro:** seed logging, env hash, pins.
* **Safety Gating:** mandatory retrieval for medicine, law, news, standards.

---

## 11) Ablations & Monitoring

Planned toggles:

1. Adapters off (cascade only).
2. Cascade off (adapters only).
3. Replay buffer off.
4. Bayes reranker off/on.
5. Dirichlet head off/on.
6. Per-skill LoRA vs single shared.

KPIs: Schema F1, Causal EM, Truth-Contract score, Retrieval ROI, Router accuracy, Addiction proxy (reward-without-truth).

---

## 12) Status & Next Actions

**Status:** Core plan drafted; not executed.
**Immediate next actions:**

1. Build seed case generator (physics + psychology).
2. Implement verifiers (truth contract, rule executor, citation aligner).
3. Run regression tests until ≥95% agreement with gold.
4. Only then wire adapters into Phi-4 trainer.

---


Do you want me to also **mock up the seed case factory design** (how to semi-automatically create JSONL cases from textbooks/papers), since that’s now the first bottleneck?
