# Wave Interaction Protocol

Use this protocol for every material event inside a Wave. Classify the event first, then use the named source of truth and owner. Do not invent an untracked side channel because a case feels urgent or unusual.

## Invariants

- An agent may originate an in-scope request or status update without main-agent pre-approval.
- Every material request, response, review finding, rework instruction, source gap, conflict, and control decision has one file-backed source of truth.
- Direct messages are optional notifications only. Mirror any material content into the required queue or control file.
- The `dependency-coordinator` routes operational dependencies; it does not review evidence, change scope or ownership, or accept artifacts.
- The reviewer decides quality findings; the original owner performs rework.
- The main agent decides scope, ownership, authorization escalation, evidence-conflict disposition at Gate, and final acceptance.
- The `handoff-steward` preserves established state across Gate, pause, recovery, and session boundaries; it does not dispatch live dependencies.
- A material event is not closed merely because a message was sent. Apply the closure condition in the routing matrix.

## Event Routing Matrix

| Wave event | Source of truth | First owner | Escalate when | Closed when |
| --- | --- | --- | --- | --- |
| Normal progress, next step, or waiting state | `status/<agent>.json` | Current agent | Waiting becomes a cross-agent dependency, source gap, or health problem | Status and timestamp reflect the new state |
| Agent A requests an artifact, answer, schema, source map, interface, or other owned output from Agent B | `queues/dependency_requests.jsonl` and `queues/dependency_responses.jsonl` | Dependency coordinator | Scope, owner, source authority, evidence conflict, authorization, or Gate decision is required | Matching response is recorded, artifact pointers resolve, requester acknowledges consumption, and waiting state is cleared |
| Several agents need the same schema, terminology, source map, interface, or assumption | `shared_contracts/<name>.md`, dependency queues, and `dependency_graph.md` | Dependency coordinator and named contract owner | No owner exists, consumers disagree materially, or a version change invalidates accepted work | Version, owner, source basis, consumers, acknowledgements, and change history are current |
| A packet becomes ready for independent review | `queues/review_queue.jsonl` and owner status | Reviewer | Review requires unavailable evidence, a scope decision, or conflicting authority | Reviewer records accept, classified rework, or a declared/source-requested gap |
| Reviewer returns a fixable finding | `queues/rework_queue.jsonl` and review record | Original artifact owner | Rework budget is exhausted, owner must change, or the flaw is systemic | Original owner submits a revised artifact and the reviewer rechecks it |
| The work needs expertise outside current packet owners | `queues/specialist_requests.jsonl` and `queues/specialist_responses.jsonl` | Requester with routed specialist | Specialist access changes scope, authorization, or safety boundary | Response and evidence pointers are recorded and consumed by the requester |
| A required file, log, dataset, connector, live system, user decision, or authority source is missing | `queues/source_requests.jsonl` and `gap_ledger.md` | Evidence owner | User action, authorization, or Gate disposition is needed | Source is provided and reviewed, an acceptable alternative closes the gap, or Gate declares a visible limitation |
| Agents disagree about source meaning, data shape, mechanism, calculation, or interpretation | `dependency_conflicts.md` plus evidence pointers | Reviewer | Conflict changes scope, authority, acceptance, or downstream plan | Reviewer or Gate records the disposition and affected claims/contracts are updated |
| Duplicate requests, stale blockers, incompatible contract versions, or circular waits appear | Dependency queues and `dependency_graph.md` | Dependency coordinator | Resolution requires scope or owner changes, user input, or Gate judgment | Duplicates are linked, cycles are broken or escalated, and all waiting states are updated |
| Two agents have overlapping write ownership or both need to modify the same artifact | Work packets, status files, and an escalation packet | Dependency coordinator detects; main agent decides | Always, unless the packet already defines one writer and one reviewer | Main agent records a single write owner or an explicit serialized handoff |
| Heartbeat, silent-window, transport, or stale-agent concern occurs | Agent status, artifact mtimes, `recovery_log.md`, and dashboard | Main agent with handoff-steward | Intervention or replacement may be required | Health is restored, a silent window is accepted, or replacement/recovery is recorded without losing ownership history |
| Gate, pause, resume, or cross-session handoff occurs | `gate_log.md`, `handoff.md`, and `recovery_log.md` | Main agent and handoff-steward | User decision or authorization is required | Accepted, unresolved, blocked, and next-action states are explicit and restartable |
| Scope, owner, source authority, authorization, or Gate decision is requested | Concise escalation packet and relevant control log | Main agent | User authority is required | Decision, rationale, affected packets, and downstream updates are recorded |

## Routing Procedure

1. Identify the event class from the matrix.
2. Write the event to its source-of-truth file before relying on notifications.
3. Assign the first owner without changing packet ownership implicitly.
4. Notify the target role if the runtime supports messaging.
5. Track the event until its closure condition is met.
6. Escalate only the smallest decision packet needed by the main agent or user.
7. Update status, dependency graph, gap ledger, review state, and handoff surfaces affected by the outcome.

If one event spans several classes, create linked records rather than overloading one queue. For example, Agent A may create a dependency request to Agent B; B may discover that the answer needs a missing source, which creates a linked source request and gap entry while the original dependency request remains blocked.
