# Loop Engineering Orchestrator

Durable Codex skill for long, evidence-heavy, or cross-functional work that should run as a controlled multi-agent loop instead of a single linear task.

The authoritative agent-facing instructions live in `SKILL.md`. This README is a short maintainer guide for the skill folder.

## What This Skill Does

`loop-engineering-orchestrator` coordinates long-running work with:

- persistent main-agent orchestration and `handoff-steward` continuity
- optional persistent `dependency-coordinator` support for high-coupling waves
- Wave0/Gate0 discovery before formal work starts
- Wave1/Wave2/...WaveN execution loops with GateN adjudication
- rolling packet-level review inside each WaveN so completed packets do not idle while other packets continue
- Output Synthesis Waves for substantial text deliverables, with execution, review, rework, and GateN inside the same wave
- subwave closeouts for WaveN1/WaveN2/... without running a strategic gate per subwave
- custom subagent routing for evidence, review, visual production, and visual skill maintenance
- claim tracing, review/rework queues, dashboard checks, and final integration discipline
- dependency request queues, dependency graphs, conflict logs, and shared contracts
- heartbeat and silent-window rules that keep long-running subagents observable without premature interruption
- network/session recovery rules that preserve original subagent ownership after manual resume

Use it when the work has multiple evidence sources, multiple agents, review/rework cycles, handoff risk, or a final deliverable that must only integrate accepted or explicitly declared-gap content.

## Core Model

The main agent and `handoff-steward` stay active from start to finish. Large waves can also activate a persistent `dependency-coordinator` so cross-agent requests, waiting-on state, and shared contracts do not crowd the main agent context. Other agents are wave-scoped and should be released, closed, or explicitly carried forward when their wave or subwave closes.

Role boundary:

- `handoff-steward` preserves continuity, stop state, accepted-vs-unresolved state, and restart instructions.
- `dependency-coordinator` manages dependency queues, shared contracts, waiting-on state, duplicate requests, stale blockers, and escalation packets.
- The main agent still owns Gate0/GateN decisions, scope changes, owner reassignment, final integration, and evidence-conflict adjudication.

Wave flow:

1. `Wave0` gathers boundaries, sources, risks, and packet recommendations.
2. `Gate0` revises scope and formal work packets from the user prompt plus Wave0 output.
3. `WaveN` runs execution, review/test, and rework capacity.
4. `GateN` accepts, rejects, declares gaps, and updates downstream plans.
5. `WaveN1/WaveN2/...` subwaves use `Subwave Closeout`, not GateN. Closeout checks completeness and acceptability, records carry-forward items, and releases or closes subwave agents.

Within a WaveN, review should be rolling: as soon as one packet reaches a review-readiness state, enqueue its reviewer and route rework back to the original owner immediately. Do not wait for every execution packet to finish unless the packet boundaries require global context.

For substantial reports, technical briefs, executive summaries, or other text deliverables, use `output-synthesizer` inside a normal Wave loop. The writer may organize and polish accepted content, but it must not create new facts, hide gaps, change claim strength, or use unaccepted artifacts as evidence.

Effort policy:

- inherit the main agent model and reasoning effort by default
- never downgrade the model
- never use `low` or `light`
- use `medium` only for simple bounded checks or post-acceptance cleanup

## Custom Agents

The skill expects these local custom agents under `C:\Users\gon56956\.codex\agents`. Those TOML files are the authoritative role definitions; the skill should route to them, not maintain looser duplicate subagent definitions:

- `handoff-steward`
- `dependency-coordinator` (optional; activate for high-coupling waves)
- `evidence-analyst`
- `output-synthesizer`
- `reviewer`
- `visual-producer`
- `visual-skill-maintainer`

If a custom agent is missing, record a control gap and block that spawn unless the user explicitly authorizes a one-off fallback packet.

## Quick Start

Initialize a control directory:

```powershell
python scripts/init_loop.py <agent_work_dir> evidence_research,document_synthesis
```

Run the dashboard check:

```powershell
python scripts/orchestrator_check.py <agent_work_dir>
```

On this Windows host, `python` may not be available. Use the bundled Codex Python runtime or another verified Python executable when needed.

## Generated Control Files

`init_loop.py` creates the standard `agent_work` surface:

- `agent_roster.md`
- `orchestration_plan.md`
- `wave_register.md`
- `source_manifest.md`
- `wave0_digest.md`
- `risk_register.md`
- `subwave_closeout_log.md`
- `gate_log.md`
- `claim_trace_matrix.md`
- `dependency_graph.md`
- `dependency_conflicts.md`
- `integration_plan.md`
- `handoff.md`
- queue files under `queues/`
- `shared_contracts/`
- persistent status files for `main-agent` and `handoff-steward`

`orchestrator_check.py` reports agent health, queue counts, missing control files, forbidden effort downgrades, model downgrade markers, and wave-scoped agents that reached terminal states without a closeout release status.

Heartbeat warnings are not termination commands. A missed heartbeat should trigger pinging and evidence checks; terminating or replacing a subagent requires main-agent review with `handoff-steward`.

Network loss or a manual session `continue` is also not a failure signal. On resume, run the dashboard, inspect status/artifacts/queues, write `recovery_log.md`, and continue existing agents where possible before spawning replacements.

## Important Files

- `SKILL.md`: main operating procedure loaded by Codex when the skill triggers.
- `references/reasoning-effort-policy.md`: effort inheritance and no-downgrade policy.
- `references/profiles.md`: profile-specific gates and acceptance expectations.
- `references/state-machine.md`: wave, subwave, review, gate, and terminal states.
- `references/status-template.json`: status-file shape for persistent and wave-scoped agents.
- `scripts/init_loop.py`: initializes a loop control directory.
- `scripts/orchestrator_check.py`: prints dashboard health and gate warnings.
- `agents/openai.yaml`: UI metadata for the skill.

## Validation

Minimum checks after editing:

```powershell
python -c "import ast, pathlib; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in pathlib.Path('scripts').glob('*.py')]"
python scripts/init_loop.py <temp_agent_work_dir> evidence_research
python scripts/orchestrator_check.py <temp_agent_work_dir>
```

The standard `quick_validate.py` skill validator may require `PyYAML`; if it fails with `ModuleNotFoundError: No module named 'yaml'`, fix the Python environment or run it with an environment that has PyYAML installed.
