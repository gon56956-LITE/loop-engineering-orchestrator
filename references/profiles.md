# Loop Engineering Task Profiles

Use these profiles to choose default work packets and gates. A task can use multiple profiles.

## evidence_research

Use for technical evidence, WI/SOP/PDF analysis, internal docs, logs, source tracing, web/internal page corroboration, or claim validation.

Default reasoning effort: inherit the main agent's effort. Use `medium` only for simple bounded source inventory.

Default gates:

- Source inventory gate
- Claim trace gate
- Conflict/gap gate
- Confidence gate
- Readability gate

Acceptance requires source references for strong claims and explicit inference labels.

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
- Reproducibility gate
- Formula/math gate
- Visualization integrity gate when charts exist
- Caveat/confidence gate

Acceptance requires schema inspection, row counts, calculation reproduction, and caveats.

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
- Audience usefulness gate
- Gap/conflict gate

Acceptance requires a coherent narrative without losing source boundaries.

## specialist_investigation

Use for targeted support such as reverse engineering, API tracing, security review, legal/source lookup, domain-specific formulas, or toolchain inspection.

Default reasoning effort: inherit the main agent's effort. Escalate when the investigation needs deeper reasoning than the main default.

Default gates:

- Request completeness gate
- Evidence response gate
- Confidence/gap gate
- Integration gate

Specialist work should answer a queued request and should not sprawl into ownership of the whole task unless reassigned by the main agent.
