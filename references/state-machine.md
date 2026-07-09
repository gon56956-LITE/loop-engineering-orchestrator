# State Machine Reference

Default states:

- wave_planned
- wave_active
- subwave_ready_for_closeout
- subwave_closeout_rework
- subwave_complete
- subwave_closed
- suspended_by_transport
- resume_pending
- recovery_review
- ready_for_gate
- gate_rework
- gate_accepted
- draft
- ready_for_trace_review
- trace_rework
- ready_for_accuracy_review
- accuracy_rework
- ready_for_depth_review
- depth_rework
- ready_for_readability_review
- readability_rework
- accepted
- visual_ready
- visual_accepted
- output_ready
- output_review
- output_rework
- output_accepted
- report_integrated
- gap

Rules:

- Wave0 is mandatory for long loop-engineering projects.
- Gate0 must revise the task plan from the user prompt plus Wave0 outputs before formal Wave1 starts.
- WaveN1/WaveN2/WaveN3 subwaves get Subwave Closeout instead of GateN. Closeout checks completeness and acceptability, records carry-forward items, and closes or releases the subwave's agents.
- Run GateN only after all subwaves for the parent WaveN are closed out or explicitly blocked.
- Keep `main-agent` and `handoff-steward` active through all waves.
- Use rolling packet-level review inside WaveN: review starts when a packet reaches `ready_for_*_review`, not only after all execution packets finish.
- Output synthesis is a normal Wave loop with execution, review, rework, and GateN; do not split output and output review into separate strategic waves.
- Network loss, UI interruption, context resume, or tool transport failure moves affected agents to `resume_pending` or `suspended_by_transport`, not failed. Recover existing ownership before spawning replacements.
- Rework against the original owner is allowed twice.
- If still blocked, assign a backup owner twice.
- If still blocked, mark `gap` with impact, confidence, and suggested next evidence.
- Never integrate `draft`, `*_rework`, stale, or unreviewed content into final output.
- Hooks may update dashboards but cannot move content to `accepted`; only main-agent adjudication or explicit reviewer output can do that.
