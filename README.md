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
- capability-based routing across custom agents and standard `explorer`, `worker`, and `default` providers
- claim tracing, review/rework queues, dashboard checks, and final integration discipline
- gap ledgers, bounded depth rework, and explicit source requests when missing evidence blocks closure
- file-backed same-Wave Agent A -> Agent B request/response routing, dependency queues, dependency graphs, conflict logs, and shared contracts
- heartbeat and silent-window rules that keep long-running subagents observable without premature interruption
- network/session recovery rules that preserve original subagent ownership after manual resume

Use it when the work has multiple evidence sources, multiple agents, review/rework cycles, handoff risk, or a final deliverable that must only integrate accepted or explicitly declared-gap content.

## Core Model

The main agent and a provider bound to the logical `handoff-steward` role stay active from start to finish. Large waves can also bind a persistent provider to `dependency-coordinator` so cross-agent requests, waiting-on state, and shared contracts do not crowd the main agent context. These providers may be matching custom agents or standard `default` agents. Other agents are wave-scoped and should be released, closed, or explicitly carried forward when their wave or subwave closes.

Role boundary:

- `handoff-steward` preserves continuity, stop state, accepted-vs-unresolved state, and restart instructions.
- `dependency-coordinator` routes same-Wave requests recorded by one execution agent for another, tracks the target response back to the requester, and manages dependency queues, shared contracts, waiting-on state, duplicate requests, stale blockers, and escalation packets. The JSONL queues are authoritative; direct messages are optional notifications only.
- The main agent still owns Gate0/GateN decisions, scope changes, owner reassignment, final integration, and evidence-conflict adjudication.

Wave flow:

1. `Wave0` gathers boundaries, sources, risks, and packet recommendations.
2. `Gate0` revises scope and formal work packets from the user prompt plus Wave0 output.
3. `WaveN` runs execution, review/test, and rework capacity.
4. `GateN` accepts, rejects, declares gaps, and updates downstream plans.
5. `WaveN1/WaveN2/...` subwaves use `Subwave Closeout`, not GateN. Closeout checks completeness and acceptability, records carry-forward items, and releases or closes subwave agents.

Within a WaveN, review should be rolling: as soon as one packet reaches a review-readiness state, enqueue its reviewer and route rework back to the original owner immediately. Do not wait for every execution packet to finish unless the packet boundaries require global context.

Gaps are tracked as work objects. Self-declared gaps, reviewer-discovered gaps, and unclosed mandatory probes go into `gap_ledger.md`; missing files, logs, data, live-system access, or user decisions go into `queues/source_requests.jsonl`. Stop rework when a defined source or authorization boundary is reached instead of letting agents speculate or loop forever.

For substantial reports, technical briefs, executive summaries, or other text deliverables, bind a suitable custom or standard provider to the logical `output-synthesizer` role inside a normal Wave loop. The writer may organize and polish accepted content, but it must not create new facts, hide gaps, change claim strength, or use unaccepted artifacts as evidence.

Effort policy:

- inherit the main agent model and reasoning effort by default
- never downgrade the model
- never use `low` or `light`
- use `medium` only for simple bounded checks or post-acceptance cleanup

## Optional Custom Agent Reference Pack

The repository ships versioned role definitions under `custom-agents/` as an optional reference pack. They are strongest for evidence/content research and for the two skill-specific control roles. The orchestrator does not require these exact TOMLs: every logical role can instead bind to a suitable standard Codex `explorer`, `worker`, or `default` agent according to `references/role-resolution.md`.

Install the custom pack only when it fits the scenario. The installer writes to `$CODEX_HOME/agents`; when `CODEX_HOME` is unset, it uses `~/.codex/agents`. Installing the skill itself does not silently modify the user's custom-agent registry.

- `handoff-steward`
- `dependency-coordinator` (optional; activate for high-coupling waves)
- `evidence-analyst`
- `output-synthesizer`
- `reviewer`
- `visual-producer`
- `visual-skill-maintainer`

Optionally install the reference roles without overwriting different same-name files:

```powershell
python scripts/install_custom_agents.py
```

Run a read-only inventory:

```powershell
python scripts/install_custom_agents.py --check
```

Existing different TOML files are reported as conflicts and preserved. Use `--force` only after reviewing the local definition and explicitly deciding to replace it.

Missing custom agents do not block startup when standard agents can satisfy the logical roles. Record a control gap only when neither an installed custom agent nor a standard `explorer`, `worker`, or `default` agent can provide the required capability.

## Quick Start

Resolve logical roles to custom or standard providers. Optionally inventory the reference custom-agent pack:

```powershell
python scripts/install_custom_agents.py --check
```

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
- `gap_ledger.md`
- `dependency_graph.md`
- `dependency_conflicts.md`
- `integration_plan.md`
- `handoff.md`
- queue files under `queues/`
- `shared_contracts/`
- persistent status files for `main-agent` and `handoff-steward`

`orchestrator_check.py` reports agent health, queue counts, open source requests, missing control files, forbidden effort downgrades, model downgrade markers, gap/source-request bookkeeping warnings, and wave-scoped agents that reached terminal states without a closeout release status.

Heartbeat warnings are not termination commands. A missed heartbeat should trigger pinging and evidence checks; terminating or replacing a subagent requires main-agent review with `handoff-steward`.

Network loss or a manual session `continue` is also not a failure signal. On resume, run the dashboard, inspect status/artifacts/queues, write `recovery_log.md`, and continue existing agents where possible before spawning replacements.

## Important Files

- `SKILL.md`: main operating procedure loaded by Codex when the skill triggers.
- `references/reasoning-effort-policy.md`: effort inheritance and no-downgrade policy.
- `references/profiles.md`: profile-specific gates and acceptance expectations.
- `references/state-machine.md`: wave, subwave, review, gate, and terminal states.
- `references/wave-interaction-protocol.md`: unified event routing matrix for Wave-internal requests, reviews, rework, gaps, conflicts, health, escalation, and handoff.
- `references/status-template.json`: status-file shape for persistent and wave-scoped agents.
- `scripts/init_loop.py`: initializes a loop control directory.
- `scripts/install_custom_agents.py`: installs or checks bundled custom-agent role definitions without overwriting conflicts by default.
- `scripts/orchestrator_check.py`: prints dashboard health and gate warnings.
- `custom-agents/`: optional versioned custom-agent reference definitions plus their scenario/lifecycle manifest.
- `agents/openai.yaml`: UI metadata for the skill.

## Validation

Minimum checks after editing:

```powershell
python -c "import ast, pathlib; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in pathlib.Path('scripts').glob('*.py')]"
python scripts/init_loop.py <temp_agent_work_dir> evidence_research
python scripts/orchestrator_check.py <temp_agent_work_dir>
```

The standard `quick_validate.py` skill validator may require `PyYAML`; if it fails with `ModuleNotFoundError: No module named 'yaml'`, fix the Python environment or run it with an environment that has PyYAML installed.
