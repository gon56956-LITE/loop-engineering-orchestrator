# Loop Engineering Task Profiles

Use these profiles to choose default work packets and gates. A task can use multiple profiles.

## evidence_research

Use for technical evidence, WI/SOP/PDF analysis, internal docs, logs, source tracing, web/internal page corroboration, or claim validation.

Default reasoning effort: inherit the main agent's effort. Use `medium` only for simple bounded source inventory.

Default gates:

- Source inventory gate
- Provenance/source-chain gate
- Internal structure/depth gate
- Claim trace gate
- Conflict/gap gate
- Gap-closure/source-request gate
- Confidence gate
- Readability gate

Acceptance requires source references for strong claims, explicit inference labels, source-chain tracing for central derived evidence, a below-surface inspection of multi-layer artifacts when nested structure or algorithm logic may affect the answer, and explicit `gap_ledger.md` / `source_requests.jsonl` entries for unclosed mandatory probes.

## code_implementation

Use for coding, bug fixes, refactors, migrations, tests, or CI fixes.

Default reasoning effort: inherit the main agent's effort.

Default gates:

- Scope/diff gate
- Test/verification gate
- Regression risk gate
- Code review gate
- Handoff gate

Acceptance requires implemented changes, relevant verification, and no unrelated churn.

## data_analysis

Use for CSV/XLSX/database analysis, KPI diagnostics, statistical summaries, or reproducible calculations.

Default reasoning effort: inherit the main agent's effort.

Default gates:

- Data quality gate
- Provenance/source-chain gate for derived extracts or metrics
- Reproducibility gate
- Formula/math gate
- Visualization integrity gate when charts exist
- Gap-closure/source-request gate
- Caveat/confidence gate

Acceptance requires schema inspection, row counts, calculation reproduction, source-chain classification for derived data, and caveats.

## visual_report

Use for charts, diagrams, HTML/PPT/PDF reports, visual explainers, or dashboards.

Default reasoning effort: inherit the main agent's effort. Use `medium` only for straightforward production from accepted specs.

Default gates:

- Source/data gate
- Visual logic gate
- Rendering gate
- Path/link gate
- Readability/layout gate

Acceptance requires SVG/PNG/PPT/HTML to render, links to resolve, and source claims to remain traceable.

## document_synthesis

Use for long-form reports, knowledge packages, executive summaries, comparison docs, or training aids.

Default reasoning effort: inherit the main agent's effort.

Default gates:

- Source coverage gate
- Structure gate
- Claim trace gate
- Output-synthesis gate when a writer agent produces the deliverable
- Audience usefulness gate
- Gap/conflict gate
- Source-request visibility gate

Acceptance requires a coherent narrative without losing source boundaries, provenance, claim strength, or declared gaps. Substantial text deliverables should be produced through an Output Synthesis Wave with reviewer and rework capacity, not by main-agent solo writing.

## output_synthesis

Use for final or interim Markdown/HTML reports, technical briefs, executive summaries, synthesis narratives, report drafts, or handoff packages built from accepted artifacts and declared gaps.

Default reasoning effort: inherit the main agent's effort. Use `medium` only for post-acceptance formatting after the synthesis is accepted.

Default gates:

- Integration-plan gate
- Accepted-artifact-only gate
- Provenance preservation gate
- Claim-strength gate
- Readability/usefulness gate
- Gap visibility gate
- Source-request visibility gate

Acceptance requires that the output uses only accepted artifacts or declared gaps, preserves provenance and confidence, keeps limitations visible, and does not make polished prose stronger than the evidence.

## Wave-Level Operating Gates

These gates apply across profiles when a loop uses multiple packets or agents:

- Rolling review gate: packet-level review starts as soon as a packet reaches a review-readiness state, without waiting for unrelated execution packets to finish.
- Rework ownership gate: review findings return to the original owner unless ownership is formally reassigned.
- Gap ledger gate: self-declared, reviewer-discovered, and mandatory-probe gaps are tracked with class, attempts, stop layer, confidence impact, and GateN disposition.
- Source request gate: missing files/data/logs/user decisions are recorded in `source_requests.jsonl` instead of being hidden as weak conclusions.
- Output integration gate: final deliverables use only accepted artifacts or declared gaps.

## specialist_investigation

Use for targeted support such as reverse engineering, API tracing, security review, legal/source lookup, domain-specific formulas, or toolchain inspection.

Default reasoning effort: inherit the main agent's effort. Escalate when the investigation needs deeper reasoning than the main default.

Default gates:

- Request completeness gate
- Evidence response gate
- Confidence/gap gate
- Integration gate

Specialist work should answer a queued request and should not sprawl into ownership of the whole task unless reassigned by the main agent.
