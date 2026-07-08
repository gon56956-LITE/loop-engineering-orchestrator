---
name: loop-engineering-orchestrator
description: Run reusable loop-engineering workflows for long, multi-agent work across research, coding, data analysis, document synthesis, visual reports, and specialist investigations. Use when Codex needs durable orchestration with persistent main-agent plus handoff-steward control, Wave0/Gate0 discovery, WaveN/GateN loops, custom subagent routing, heartbeat status, request/rework queues, claim trace matrices, owner-preserving review/rework gates, quality checks, hooks, dashboards, handoffs, and final integration discipline.
---

# Loop Engineering Orchestrator

Use this skill when the work is too long, risky, cross-functional, or evidence-heavy to treat as a single linear task. The skill is domain-neutral: it coordinates the loop, not the subject matter.

## Core Idea

The main agent is the orchestrator. `handoff-steward` is the persistent continuity partner. Other subagents are wave-scoped workers, analysts, reviewers, visual producers, maintainers, testers, or rework owners. Hooks and scripts only observe state and run checks; they never replace main-agent judgment.

A successful loop has six durable surfaces:

1. `agent_work/` control directory for state and handoff.
2. Persistent control pair: main agent plus `handoff-steward` active from start to finish.
3. Intake, source, risk, wave, and orchestration plans that define the work before agents run.
4. Wave-scoped work packets that tell each agent exactly what it owns.
5. Claim trace matrix that links claims to evidence, logic, outputs, and review status.
6. Review/rework gates that stop weak work before final integration.
7. Handoff and integration files that let a new session resume without guesswork.

## Custom Agent Roster

Use custom agents from `C:\Users\gon56956\.codex\agents` when spawning subagents. These TOML files are the authoritative role definitions; this skill only routes work to them and adds loop-level controls. Do not define shadow subagents inside the skill.

- `handoff-steward`: persistent loop checkpoint and continuity agent. Keep active from loop start through final handoff. Use for accepted-vs-unresolved state, stop states, authorization boundaries, current artifact paths, next-action queues, and startup prompts. Do not use it as the reviewer or primary analyst.
- `evidence-analyst`: wave-scoped execution agent for source-bound technical evidence work across PDFs, WI/docs, HTML/Markdown, CSV/XLSX, .cal files, logs, configs, recipes, test outputs, and source-code tracing.
- `reviewer`: wave-scoped independent review/test/QA agent. Use to decide whether outputs satisfy requirements, evidence quality, code/test expectations, visual QA, skill compliance, or gate readiness.
- `visual-producer`: wave-scoped execution agent for one-off charts, diagrams, PPT/PPTX, HTML slide decks, PNG posts, image batches, visual reports, and presentation-ready artifacts.
- `visual-skill-maintainer`: wave-scoped specialist for modifying reusable visual generation skills, renderers, recipes, palettes, fixtures, galleries, tests, and release flows.

If a needed custom agent is unavailable, do not silently emulate it. Record the missing agent as a control gap and block spawning that role unless the user explicitly authorizes a one-off fallback packet.

## Task Profiles

Choose one or more profiles before spawning agents. Read `references/profiles.md` when choosing gates and `references/reasoning-effort-policy.md` when assigning reasoning effort.

- `evidence_research`: source-bound analysis across documents, logs, web/internal pages, data exports, PDFs, code, or other evidence.
- `code_implementation`: implementation or refactor work with tests, diff review, and regression risk control.
- `data_analysis`: metric, CSV/XLSX/database, statistical, or diagnostic analysis requiring reproducible calculations.
- `visual_report`: charts, diagrams, HTML/PPT/PDF reports, screenshots, or visual QA.
- `document_synthesis`: WI/SOP/doc synthesis, knowledge packages, comparison reports, or executive narratives.
- `specialist_investigation`: targeted expert support such as reverse engineering, API tracing, security review, legal-source lookup, or domain-specific validation.

## Reasoning Effort Policy

Use a quality-first effort policy. Subagents inherit the main agent's model and reasoning effort by default. Never assign a weaker model than the main agent or the user-requested model.

- `medium`: allowed only for simple bounded work such as post-acceptance formatting, path/link/file checks, queue counting, dashboard summaries, or already-specified visual production.
- `high` or above: use for evidence research, code implementation, data analysis, document synthesis, complex visuals, review gates, rework, and integration.
- `xhigh`: use when inherited from the main agent or when explicitly needed for reverse engineering, algorithm confirmation, high-risk math, trace-integrity review, source-conflict adjudication, repeated rework, and final claim integration.

Every work packet should declare the default effort, escalation triggers, downgrade triggers, and any concurrency constraint. Status files should include `reasoning_effort` and `effort_rationale`. Specialist requests should include `requested_reasoning_effort`.

Do not use `low` or `light` effort in loop-engineering work. If a custom-agent default is lower than the main agent's current effort, explicitly request inherited effort or record the downgrade as a gate blocker.

## Intake And Plan Shape

Before creating work packets, classify the requested loop and write the plan spine into `orchestration_plan.md`, `source_manifest.md`, and `risk_register.md`.

Answer these questions explicitly:

- Mission: what final artifact or decision must exist at the end?
- Hard constraints: what must not be touched, executed, overwritten, degraded, or inferred?
- Source authority: which files, systems, logs, docs, tests, or people are authoritative, and which are only supporting context?
- Unknowns: what must Wave 0 discover before later agents can work safely?
- Work shape: which profiles apply, which roles are independent, and which dependencies force sequencing?
- Wave shape: why Wave0 is needed, how formal Wave1/Wave2/...WaveN work should be staged, and whether any WaveN needs subwaves such as WaveN1/WaveN2/WaveN3.
- Review ownership: who executes, who reviews/tests, which rework agents are reserved, and when a backup owner can take over?
- Integration barrier: what evidence, tests, rendering checks, or gap declarations must exist before content can enter the final deliverable?

If missing information could cause the wrong files, data, live systems, or behavior to be changed, stop and ask one concise clarification question. If the user has already given hard constraints, encode them in the control files rather than leaving them only in chat.

## Standard Workflow

1. Initialize `agent_work/` with `scripts/init_loop.py <agent_work_dir> [comma_separated_profiles]`.
2. Start the persistent control pair: main agent plus `handoff-steward`. Keep both active until final handoff.
3. Write `agent_roster.md`, `orchestration_plan.md`, `source_manifest.md`, `wave_register.md`, and `risk_register.md`.
4. Plan and run Wave0 for boundary discovery, source inventory, task partitioning, risk discovery, and formal packet recommendations.
5. Gate0: main agent adjudicates Wave0 with `handoff-steward`, combines the user prompt, hard constraints, Wave0 output, and discovered evidence, then revises task details before formal work starts.
6. Plan formal Wave1/Wave2/...WaveN loops. Each WaveN must include execution agents, review/test agents, and reserved rework agents.
7. If WaveN is too large, split it into WaveN1/WaveN2/WaveN3 subwaves. Each subwave gets a Subwave Closeout: check output completeness and acceptability, record carry-forward items, close or release that subwave's agents, and update `subwave_closeout_log.md`. Run one GateN after the whole WaveN completes.
8. Spawn wave-scoped subagents only after the user has authorized subagents or parallel agent work. Close or release subwave agents at Subwave Closeout, and close or release parent-wave agents after GateN accepts, declares gaps, or formally carries items forward.
9. Give each subagent a status file, owned artifact path, inherited model/effort policy, acceptance criteria, source boundaries, claim-trace obligations, and review or rework path.
10. Require heartbeat updates every 10 minutes or a bounded silent window declaration.
11. Use `scripts/orchestrator_check.py <agent_work_dir>` between waits to inspect health, queues, missing controls, downgrade warnings, and quality warnings.
12. Route findings back to the original owner for rework unless the rework limit is reached or the owner is explicitly reassigned.
13. GateN: main agent adjudicates accepted outputs, rejected outputs, declared gaps, and downstream plan changes with `handoff-steward`; update `gate_log.md`, `handoff.md`, and next wave packets.
14. Write `integration_plan.md` before final assembly, mapping each final section or output to accepted artifacts or declared gaps.
15. Integrate only accepted or declared-gap content into the final deliverable, then refresh `handoff.md`.

## Directory Contract

`agent_work/` should contain:

- `status/*.json`: one heartbeat/status file per agent.
- `artifacts/*.md`: analyst/worker outputs and accepted evidence summaries.
- `work_packets/*.md`: main-agent assignments.
- `waves/`: optional per-wave folders for packets, outputs, completeness checks, and gate prep.
- `queues/specialist_requests.jsonl`: requests for specialist help.
- `queues/specialist_responses.jsonl`: specialist answers.
- `queues/review_queue.jsonl`: review tasks.
- `queues/visual_queue.jsonl`: visual production/review tasks.
- `queues/rework_queue.jsonl`: queued rework assignments and backup-owner transfers.
- `claim_trace_matrix.md`: claim/evidence/logic/review trace spine.
- `agent_roster.md`: persistent agents, wave-scoped agents, reserved rework agents, and role routing.
- `orchestration_plan.md`: mission, constraints, profiles, waves, roles, dependencies, and stop conditions.
- `source_manifest.md`: authoritative sources, supporting sources, missing sources, and unsafe/live surfaces.
- `wave_register.md`: Wave0, formal WaveN loops, subwaves, owners, gate status, and carry-forward items.
- `subwave_closeout_log.md`: subwave completeness, acceptability, released agents, carry-forward items, and unresolved rework.
- `wave0_digest.md`: shared discovery results and packet recommendations.
- `risk_register.md`: failure modes, mitigations, owners, and verification hooks.
- `recovery_log.md`: network/session interruptions, resume decisions, preserved agents, restarted agents, and evidence used for recovery.
- `gate_log.md`: Gate0/GateN decisions, accepted outputs, rejected outputs, declared gaps, and next-wave changes.
- `integration_plan.md`: final assembly map from deliverable sections to accepted artifacts or declared gaps.
- `handoff.md`: current state, next actions, blockers, and resume instructions.
- `review_log.md`, `visual_review_log.md`, `hooks_log.md`, `orchestrator_state.json`.
- `reports/`: final or interim integrated deliverables.

Compatibility aliases may exist for older loops, such as `re_requests.jsonl`, `re_responses.jsonl`, and `trace_matrix.md`. Prefer the generic names for new work.

## Wave And Packet Rules

Wave0 is mandatory for any long loop-engineering project. It is for shared discovery, not final answers. Its outputs should identify source groups, authority conflicts, missing evidence, likely packet boundaries, unsafe actions, and questions that would block downstream work.

Gate0 happens after Wave0. The main agent uses Gate0 to combine the user prompt, Wave0 findings, hard constraints, and source inventory, then corrects the scope, wave plan, packets, review plan, and risk register before formal work starts.

Formal work runs as Wave1/Wave2/...WaveN. Each WaveN can be research, coding, data analysis, visual production, report writing, skill maintenance, review, or mixed work. Each WaveN has one GateN.

Subwaves such as WaveN1/WaveN2/WaveN3 are allowed when a WaveN has too many tasks. A subwave is still a complete operational loop: plan, spawn, execute, review/test, rework as needed, close out, and release its wave-scoped agents. It does not get a strategic GateN.

At Subwave Closeout, the main agent and `handoff-steward` confirm:

- all expected artifacts exist and are readable
- review/test outputs exist or the missing review is logged as a blocker
- accepted, rejected, rework, and carry-forward items are separated
- claim-trace rows, queues, and artifact paths are updated
- subwave-scoped agents are closed, released, or explicitly carried forward with a reason
- downstream impacts are recorded for the parent WaveN gate

Do not run a full GateN until all subwaves for that WaveN are closed out or explicitly declared blocked. GateN adjudicates the parent wave using all subwave closeouts together.

Every WaveN must reserve:

- execution agents for the work itself
- review/test agents for acceptance checks
- rework agents or backup owners for fixes after review

For broad research with many topics, split work by topic or source family and assign parallel evidence packets plus parallel reviewer packets. Do not rely on one human review pass to discover shallow analysis across many topics. Review packets should check depth, source coverage, and internal-logic trace for the same topic boundary as the evidence packet.

When the topic class is new, the source structure is unfamiliar, or prior analyst output was too shallow, run one calibration packet before scaling parallel work. The calibration packet must produce a depth trace and mechanism narrative, pass reviewer explain-back, and become the packet template for the remaining topics. Do not launch a large parallel wave from an unproven shallow packet shape.

For each evidence packet over multi-layer files, include a depth contract:

- map outer file structure and relevant inner structures
- trace source fields or inputs through transformations, algorithms, formulas, recipes, code paths, or log phases to outputs
- identify uninspected lower layers as explicit gaps
- require a reviewer to check depth before acceptance

Each work packet should include:

- `packet_id`, `wave_id`, optional `subwave_id`, role, custom agent type, owner, reviewer, rework owner, status path, and owned artifact path.
- Mission question, in-scope sources, out-of-scope sources, and hard constraints.
- Expected output shape, claim-trace obligations, acceptance gates, and rework route.
- Depth contract for multi-layer artifacts, including required internal structure map and input -> transformation -> output trace.
- Mechanism narrative requirement for research-like work: explain the mechanism in natural human language after the trace, not as raw extraction notes.
- Inherited model/effort policy, allowed downgrade only to `medium` for simple bounded work, escalation triggers, concurrency notes, and silent-window expectations.
- Dependencies on earlier packets, specialist requests, visual tasks, or user decisions.

Do not spawn two agents with overlapping write ownership. If two agents need the same source set, separate their questions or make one a reviewer.

## Agent Status Rules

Each status file must include:

- `agent_id`, `role`, `custom_agent`, `lifecycle`, `wave_id`, `profile`, `reasoning_effort`, `effort_rationale`, `model_policy`, `state`, `current_artifact`, `last_progress_at`, `next_step`, `blockers`.
- Use optional `subwave_id` for subwave agents and `release_status` for wave-scoped agents at closeout. Valid closeout release statuses are `released`, `closed`, and `carried_forward`.
- Optional `heartbeat_interval_minutes`, `last_heartbeat_at`, `silent_window_until`, `silent_window_reason`, `last_ping_at`, `ping_count`, and `do_not_interrupt_before` for long processing.
- Optional `rework_count`, `accepted`, and `gap_declared`.

Use `lifecycle: persistent` for `main-agent` and `handoff-steward`; use `lifecycle: wave_scoped` for other subagents.

## Heartbeat And Non-Interruption Policy

Heartbeat is a protection mechanism, not a timer for termination. Its purpose is to keep long-running subagents observable while preventing the main agent from interrupting useful work too early.

Default heartbeat interval is 10 minutes. A subagent doing long reading, rendering, analysis, tests, or synthesis may declare a bounded silent window by setting `silent_window_until` and `silent_window_reason`. During that window, treat no-update behavior as expected unless the agent exceeds the window materially.

When a heartbeat is missed:

- After one missed heartbeat, mark `needs_ping` and send a lightweight status ping. Do not reassign or terminate.
- After two missed checks, mark `potentially_stuck`; inspect the status file, owned artifact mtime, queue activity, logs, and declared silent window before deciding anything.
- After three missed checks, mark `intervene`; intervention means main-agent review with `handoff-steward`, not automatic cancellation.
- Before terminating, replacing, or reassigning a subagent, confirm all of these are true: no unexpired silent window, no recent owned-artifact updates, no queue response in progress, no declared long-running command/test/render, and no user requirement to keep the original owner active.
- If the agent is likely still productively working, extend or record a new silent window rather than interrupting.

Hooks and dashboards may raise stale-agent warnings, but they cannot kill, close, reassign, or accept work. Only the main agent can decide intervention after checking the evidence above.

## Network And Session Recovery

Treat network loss, UI interruption, context resume, or tool transport failure as a recovery event, not as subagent failure.

On resume after an interruption:

1. Freeze orchestration. Do not spawn replacement agents, kill old agents, or reassign ownership yet.
2. Run `scripts/orchestrator_check.py <agent_work_dir>` and read `last_dashboard.md`, `hooks_log.md`, status files, owned artifact mtimes, queues, and any partial outputs.
3. Mark affected active agents as `resume_pending` or `suspended_by_transport` only if their status is stale because the parent session was interrupted.
4. Ask whether the original subagent work can continue from existing artifacts and status. Prefer continuing the original agent ownership when any useful state remains.
5. Use `handoff-steward` to write a recovery note into `recovery_log.md`: interruption time, affected agents, latest known artifacts, preserved work, lost work, and resume decision.
6. Resume existing agents when possible. If the tool cannot continue the original subagent, create a replacement only after recording `restart_reason: transport_unrecoverable` and linking the previous status/artifacts.
7. Never restart a whole wave merely because the parent session required a manual "continue". Restart only the missing packet or agent, and preserve accepted or partial outputs.

Replacement agents must receive the previous agent's status path, artifact path, queues, and recovery note. They should continue or repair the prior work, not redo it from scratch unless the recovery log says the prior artifacts are unusable.

Health labels:

- `healthy`: status or owned artifact updated within the heartbeat window.
- `quiet_expected`: no update, but an unexpired silent window exists.
- `needs_ping`: missed heartbeat once.
- `potentially_stuck`: missed two checks.
- `intervene`: missed three checks or exceeded silent window materially.

Do not kill work by elapsed time alone. Use status timestamps, owned artifact mtimes, declared silent windows, and ping history together.

## Request Queue Rules

Use `specialist_requests.jsonl` for cross-agent dependencies. This avoids untracked side chats and gives the main agent a queue to prioritize.

Each request should include:

- `id`, `created_at`, `requester`, `specialty`, `priority`, `status`.
- `requested_reasoning_effort`, `question`, `context`, `evidence_pointers`, `expected_output`, `blocking_claims`.

Each response should include:

- `request_id`, `responder`, `status`, `answer`, `evidence_pointers`, `confidence`, `gaps`, `followups`.

Examples of `specialty`: `reverse_engineering`, `math_check`, `api_contract`, `source_lookup`, `visual_design`, `security_review`, `domain_expert`.

## Review Gates

Use this default state machine:

`draft -> ready_for_trace_review -> trace_rework|ready_for_accuracy_review -> accuracy_rework|ready_for_depth_review -> depth_rework|ready_for_readability_review -> readability_rework|accepted -> visual_ready -> visual_accepted -> report_integrated`

Map gates to the task profile:

- Evidence/source gate: every strong claim has a source or is labeled inference.
- Trace/logic gate: inputs, transformations, outputs, and claims form a coherent chain.
- Internal-structure gate: multi-layer files were inspected below the surface layer, and algorithm/control-flow claims include source-backed mechanisms.
- Accuracy/math/test gate: calculations, code, tests, thresholds, and comparisons are correct.
- Analysis-depth gate: the work answers the relevant why/how/what/when/where/who questions.
- Explain-back gate: a technical human can reconstruct the mechanism, evidence chain, limitations, and practical meaning from the narrative without reading raw extraction notes.
- Readability/usefulness gate: the target audience can use the result.
- Artifact gate: files open, links resolve, diagrams/charts render, outputs are complete.

Rework limit: original owner gets up to 2 rework attempts. If still blocked, assign a backup owner up to 2 attempts. If still unresolved, mark a gap with impact and confidence.

Reviewers classify issues and cite evidence; they should not silently absorb the fix into central integration unless the owner is unavailable and the ownership change is recorded. Keep the original owner attached to the artifact until it is accepted, declared as a gap, or formally reassigned.

Gate0 and GateN are main-agent decisions, not reviewer-only decisions. The reviewer can recommend accept/revise/reject, but the main agent records the gate decision after consulting the trace matrix, review output, risk register, and handoff-steward state.

## Hooks

If Codex hooks are enabled, use `scripts/codex_hook.ps1` to append lightweight events and refresh `last_dashboard.md` when an `agent_work/` directory exists. Hooks should be safe and local: no network, no external writes, no source mutation beyond loop control files.

Hooks are useful for:

- Heartbeat and stale-agent detection.
- Artifact discovery after writes.
- Lightweight quality warnings.
- Stop-time dashboard refresh.

Hooks are observation-only. They should never interrupt long-running work, mutate source artifacts, close agents, or replace the main-agent plus `handoff-steward` intervention decision.

## Verification

Run:

`python scripts/orchestrator_check.py <agent_work_dir>`

Before final integration, confirm:

- required active agents are not stale or unaccounted for
- `main-agent` and `handoff-steward` status files exist and are current
- no agent status records `low`, `light`, or model downgrade
- `orchestration_plan.md`, `source_manifest.md`, `risk_register.md`, and `integration_plan.md` exist and match current scope
- Wave0/Gate0 are complete before formal Wave1 starts
- each WaveN has execution, review/test, and rework capacity assigned before it starts
- each completed subwave has a closeout entry and its subagents are closed, released, or explicitly carried forward
- all accepted artifacts passed their gates
- unresolved claims are marked as gaps, not quietly integrated
- final deliverables reference only existing reviewed artifacts
- handoff files are current enough for a new session to resume safely
