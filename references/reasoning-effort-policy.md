# Reasoning Effort Policy

Use this policy to assign model and reasoning effort for long loop-engineering work.

## Strategy

Default strategy: inherit first, quality first.

- Inherit the main agent's model and reasoning effort for every subagent by default.
- Never assign a weaker model than the main agent or the user-requested model.
- Never use `low` or `light` effort in loop-engineering work.
- Downgrade only to `medium`, and only for simple bounded work.
- Use inherited or higher effort for cross-evidence analysis, implementation, review gates, rework, and final claim integration.
- A work packet should include the inherited default, allowed escalation, and any medium-only downgrade condition.

## Tier Guide

- `medium`: post-acceptance formatting, path/link/file checks, queue counting, dashboard summaries, already-specified visual production, and other simple bounded work.
- `high`: evidence research, code implementation, data analysis, document synthesis, complex visuals, cross-source reconciliation, and most analyst/reviewer work.
- `xhigh`: reverse engineering, algorithm confirmation, high-risk math, trace-integrity review, source-conflict adjudication, repeated rework, backup analyst rescue, and final accepted-claim closure.

If the main agent is running at `xhigh`, subagents inherit `xhigh` unless the task is simple enough to justify `medium`. Do not drop from `xhigh` to `high` just to reduce resource use.

## Profile Defaults

- `evidence_research`: inherit main effort
- `code_implementation`: inherit main effort
- `data_analysis`: inherit main effort
- `visual_report`: inherit main effort; `medium` allowed for already-specified simple production
- `document_synthesis`: inherit main effort
- `output_synthesis`: inherit main effort; `medium` allowed only for post-acceptance formatting
- `specialist_investigation`: inherit main effort; escalate if reverse engineering, math, or conflict adjudication needs more

## Escalation Triggers

Escalate above `medium` when work involves:

- cross-file or cross-source dependencies
- source conflicts
- reproducible calculations
- workflow branch interpretation
- data quality judgment
- visual logic design

Escalate to `xhigh` when work involves:

- algorithm formulas or threshold derivation
- reverse engineering or bytecode/IL/decompile analysis
- high-risk math review
- source-of-truth conflict adjudication
- two failed rework rounds
- final report claim integration
- output synthesis that must preserve provenance and claim strength across many accepted artifacts
- security, legal, medical, financial, or other high-stakes interpretation

## Downgrade Triggers

Downgrade to `medium` only when work is:

- post-acceptance formatting
- path/link/file existence checking
- dashboard or heartbeat reporting
- queue counting
- SVG/JSON pairing
- deterministic output cleanup after the logic is accepted

## Forbidden Downgrades

- Do not use `low` or `light`.
- Do not choose a weaker model than the main agent or user-requested model.
- Do not let a custom-agent TOML default silently lower effort. Override it in the spawn request or record a gate blocker.
- Do not cap `high` or `xhigh` concurrency inside this skill. Manage concurrency by wave scope, write ownership, dependency order, and user authorization.

## Required Fields

`status/<agent>.json` should include:

- `reasoning_effort`
- `effort_rationale`
- `model_policy`

`work_packets/*.md` should include:

- inherited model and effort default
- allowed escalation range, if any
- escalation triggers
- `medium` downgrade triggers, if any
- concurrency or silent-window notes

`queues/specialist_requests.jsonl` should include:

- `requested_reasoning_effort`

`queues/dependency_requests.jsonl` should include:

- `requested_reasoning_effort`

Missing effort fields are warnings for older loops, not fatal errors.
