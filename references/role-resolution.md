# Role Resolution

Treat Loop roles as capability contracts, not fixed custom-agent names. Resolve a provider for each role when planning the Wave, record the binding in `agent_roster.md` and status files, and keep the same review, ownership, effort, queue, and Gate rules regardless of provider.

## Provider Order

1. Use a custom agent when its instructions, tools, model/effort, and domain fit the packet.
2. Otherwise use a standard Codex agent type with an explicit role packet.
3. Create a control gap only when neither a suitable custom agent nor a standard agent can satisfy the required capability.

Missing a particular custom TOML is not itself a blocker. A standard provider is a normal supported route, not a one-off fallback.

## Standard Codex Agent Types

- `explorer`: read-only discovery and specific codebase/repository questions. Use for code navigation, caller tracing, file inventory, and bounded source inspection. Do not assign write ownership.
- `worker`: execution and production with an explicit, non-overlapping write scope. Use for coding, data-processing scripts, report artifacts, visual artifacts, and rework by the original owner.
- `default`: general reasoning, coordination, synthesis, non-code research, independent review, handoff continuity, and dependency coordination when no more specific custom role is installed.

Use separate agent instances for execution and independent review even when they share the same standard agent type.

## Capability Mapping

| Logical Wave role | Preferred custom example | Standard provider |
| --- | --- | --- |
| Wave0 source/code discovery | `evidence-analyst` for evidence research | `explorer` for codebase/repository discovery; `default` for documents, data, or mixed research |
| Coding or artifact implementation | Domain-specific implementation agent | `worker` with exclusive file ownership |
| Large-scale data analysis | Data-analysis custom agent | `worker` for reproducible scripts/artifacts; `default` for bounded analytical reasoning |
| Evidence/content research | `evidence-analyst` | `default`, or `explorer` when the question is specifically codebase-bound |
| Independent review/test/QA | `reviewer` | Separate `default`; use `explorer` for bounded read-only code inspection |
| Rework | Original custom execution owner | Original `worker` or original standard execution owner |
| Large text/output synthesis | `output-synthesizer` | `worker` for file-backed deliverables; `default` for bounded text synthesis |
| Visual production | `visual-producer` | `worker` or `default` using the selected visual skill |
| Visual-skill maintenance | `visual-skill-maintainer` | `worker` with the target visual skill/repo as exclusive write scope |
| Dependency coordination | `dependency-coordinator` | Persistent `default` with the dependency-coordination packet and queue ownership |
| Handoff continuity | `handoff-steward` | Persistent `default` with the handoff/checkpoint packet |
| Specialist investigation | Matching specialist custom agent | `default`, `explorer`, or `worker` according to whether the packet is general, read-only code discovery, or artifact-producing |

## Scenario Guidance

### Evidence And Content Research

The bundled custom-agent pack is strongest here. Use its provenance, depth, source-request, review, and output-synthesis behavior as a reference implementation. Do not assume those prompts are optimal for coding, quantitative analysis, or every content domain.

### Coding

Use `explorer` for bounded codebase questions, `worker` for implementation with exclusive file ownership, a separate reviewer provider for diff/test review, and the original worker for rework. Do not force coding work through `evidence-analyst`.

### Large-Scale Data Analysis

Split source/data discovery, reproducible computation, result validation, and narrative synthesis into separate packets. Use workers for scripts/notebooks/artifacts and a separate default reviewer for methodology, calculation, and interpretation checks.

### Large-Scale Content Output

Separate source research, outline/claim integration, drafting, review, and rework. A standard worker can own the output file, while a separate default agent reviews claim strength, completeness, and audience usefulness.

## Binding Record

For each active role, record:

- `role_binding`: logical role such as `reviewer`, `dependency-coordinator`, or `output-synthesizer`
- `provider_kind`: `custom` or `standard`
- `agent_type`: actual custom name or one of `explorer`, `worker`, `default`
- `binding_rationale`: why this provider fits the packet
- model/effort policy, lifecycle, Wave/subwave, owned artifact, review/rework path, and release status

Do not label a standard agent as if its custom TOML were installed. The logical role may be the same, but the provider must remain explicit.

The dashboard machine-checks the standard mappings for core logical roles. Domain-specific role names remain extensible, but they still require a valid provider type and a non-empty `binding_rationale` so the binding is auditable.

Custom providers are not limited to the bundled reference pack. When a status binds a user-defined custom agent, the dashboard validates that agent's installed TOML on demand and records it in the inventory. The custom name must be a simple local agent identifier, and the TOML `name` must match it.

## Resolution Gate

Before spawning a Wave:

1. List the logical roles required by the packets.
2. Inventory installed custom agents and available standard agent types.
3. Bind each logical role to a provider.
4. Confirm execution and independent review use separate instances.
5. Confirm workers have non-overlapping write scopes.
6. Confirm persistent control roles have a custom or standard provider.
7. Record unresolved capabilities as control gaps.

The Wave may proceed when every required capability has a provider, even if no optional custom agents are installed.
