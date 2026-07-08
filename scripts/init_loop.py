#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_STATE = {
    "version": 3,
    "created_at": None,
    "phase": "initialized",
    "active_wave": "Wave0",
    "active_gate": "Gate0",
    "heartbeat_minutes": 10,
    "ping_after_missed": 1,
    "intervene_after_missed": 3,
    "profiles": [],
    "persistent_agents": ["main-agent", "handoff-steward"],
    "wave_policy": {
        "wave0_required": True,
        "gate_after_each_formal_wave": True,
        "subwaves_skip_gate": True,
        "subwaves_require_closeout_without_gate": True,
        "require_execution_review_rework_capacity": True,
    },
    "effort_policy": {
        "strategy": "inherit_main_quality_first",
        "inherit_main_model": True,
        "inherit_main_effort": True,
        "model_downgrade_allowed": False,
        "minimum_effort": "medium",
        "forbidden_efforts": ["low", "light"],
        "profile_defaults": {
            "evidence_research": "inherit_main",
            "code_implementation": "inherit_main",
            "data_analysis": "inherit_main",
            "visual_report": "inherit_main_or_medium_when_simple",
            "document_synthesis": "inherit_main",
            "specialist_investigation": "inherit_main"
        },
        "missing_effort_is_warning": True
    },
    "integration_policy": {
        "accepted_or_declared_gap_only": True,
        "preserve_original_owner_rework": True
    },
}
ROOT_FILES = [
    "agent_roster.md",
    "orchestration_plan.md",
    "wave_register.md",
    "claim_trace_matrix.md",
    "trace_matrix.md",
    "source_manifest.md",
    "wave0_digest.md",
    "risk_register.md",
    "recovery_log.md",
    "subwave_closeout_log.md",
    "gate_log.md",
    "integration_plan.md",
    "handoff.md",
    "review_log.md",
    "visual_review_log.md",
    "hooks_log.md",
]
QUEUE_FILES = [
    "specialist_requests.jsonl",
    "specialist_responses.jsonl",
    "re_requests.jsonl",
    "re_responses.jsonl",
    "review_queue.jsonl",
    "visual_queue.jsonl",
    "rework_queue.jsonl",
]

def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def initial_content(name):
    title = name.replace("_", " ").replace(".md", "").title()
    initialized = now_iso()
    templates = {
        "agent_roster.md": [
            "# Agent Roster",
            "",
            f"Initialized: {initialized}",
            "",
            "## Persistent Agents",
            "",
            "- main-agent: orchestrator and final gate decision owner",
            "- handoff-steward: continuity, stop-state, accepted-vs-unresolved, and next-action owner",
            "",
            "## Wave-Scoped Custom Agents",
            "",
            "- evidence-analyst: source-bound evidence execution",
            "- reviewer: independent review, test, and QA",
            "- visual-producer: one-off visual deliverables",
            "- visual-skill-maintainer: reusable visual skill/tool maintenance",
            "",
            "## Reserved Rework Capacity",
            "",
        ],
        "orchestration_plan.md": [
            "# Orchestration Plan",
            "",
            f"Initialized: {initialized}",
            "",
            "## Mission",
            "",
            "## Deliverables",
            "",
            "## Hard Constraints",
            "",
            "## Persistent Control Pair",
            "",
            "## Profiles And Waves",
            "",
            "## Roles And Dependencies",
            "",
            "## Stop Conditions",
            "",
        ],
        "wave_register.md": [
            "# Wave Register",
            "",
            f"Initialized: {initialized}",
            "",
            "| Wave | Subwaves | Purpose | Execution Agents | Review/Test Agents | Rework Capacity | Gate | Status |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
            "| Wave0 | | Discovery, boundaries, source inventory, packet recommendations | | | | Gate0 | planned |",
        ],
        "source_manifest.md": [
            "# Source Manifest",
            "",
            f"Initialized: {initialized}",
            "",
            "## Authoritative Sources",
            "",
            "## Supporting Sources",
            "",
            "## Missing Or Unavailable Sources",
            "",
            "## Unsafe Or Live Surfaces",
            "",
        ],
        "wave0_digest.md": [
            "# Wave0 Digest",
            "",
            f"Initialized: {initialized}",
            "",
            "## Shared Discoveries",
            "",
            "## Conflicts And Gaps",
            "",
            "## Recommended Work Packets",
            "",
        ],
        "risk_register.md": [
            "# Risk Register",
            "",
            f"Initialized: {initialized}",
            "",
            "| Risk | Impact | Mitigation | Owner | Verification | Status |",
            "| --- | --- | --- | --- | --- | --- |",
        ],
        "recovery_log.md": [
            "# Recovery Log",
            "",
            f"Initialized: {initialized}",
            "",
            "| Time | Event | Affected Agents | Preserved Artifacts | Lost Work | Resume Decision | Restart Reason | Owner |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ],
        "subwave_closeout_log.md": [
            "# Subwave Closeout Log",
            "",
            f"Initialized: {initialized}",
            "",
            "| Subwave | Expected Artifacts | Review/Test Status | Acceptability | Released Agents | Carry-Forward Items | Blockers | Owner |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ],
        "gate_log.md": [
            "# Gate Log",
            "",
            f"Initialized: {initialized}",
            "",
            "| Gate | Inputs | Decision | Accepted | Rework | Gaps | Next Wave Changes | Owner |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ],
        "integration_plan.md": [
            "# Integration Plan",
            "",
            f"Initialized: {initialized}",
            "",
            "| Final Output Section | Source Artifact | Gate Status | Gaps | Integration Owner |",
            "| --- | --- | --- | --- | --- |",
        ],
        "handoff.md": [
            "# Handoff",
            "",
            f"Initialized: {initialized}",
            "",
            "## Current State",
            "",
            "## Accepted Artifacts",
            "",
            "## Declared Gaps",
            "",
            "## Active Blockers",
            "",
            "## Next Actions",
            "",
        ],
    }
    return "\n".join(templates.get(name, [f"# {title}", "", f"Initialized: {initialized}", ""])) + "\n"

def status_content(agent_id, role, custom_agent):
    now = now_iso()
    return {
        "agent_id": agent_id,
        "role": role,
        "custom_agent": custom_agent,
        "lifecycle": "persistent",
        "wave_id": "all",
        "profile": "orchestration",
        "reasoning_effort": "inherit_main",
        "effort_rationale": "Persistent loop control inherits the main agent effort; no low/light downgrade is allowed.",
        "model_policy": "inherit_main_model_no_downgrade",
        "state": "active",
        "current_artifact": "agent_work/handoff.md" if agent_id == "handoff-steward" else "agent_work/orchestration_plan.md",
        "last_progress_at": now,
        "next_step": "Maintain loop continuity" if agent_id == "handoff-steward" else "Plan and adjudicate Wave0",
        "blockers": [],
        "silent_window_until": None,
        "silent_window_reason": None,
        "rework_count": 0,
        "accepted": False,
        "gap_declared": False,
    }

def ensure_persistent_statuses(root):
    status_dir = root / "status"
    defaults = [
        ("main-agent", "Orchestrator", "main-agent"),
        ("handoff-steward", "Handoff Steward", "handoff-steward"),
    ]
    for agent_id, role, custom_agent in defaults:
        path = status_dir / f"{agent_id}.json"
        if not path.exists():
            path.write_text(json.dumps(status_content(agent_id, role, custom_agent), indent=2), encoding="utf-8")

def main():
    if len(sys.argv) not in (2, 3):
        print("usage: init_loop.py <agent_work_dir> [comma_separated_profiles]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    profiles = [p.strip() for p in sys.argv[2].split(",") if p.strip()] if len(sys.argv) == 3 else []
    for rel in ["status", "queues", "artifacts", "work_packets", "waves", "reports"]:
        (root / rel).mkdir(parents=True, exist_ok=True)
    for name in ROOT_FILES:
        p = root / name
        if not p.exists():
            p.write_text(initial_content(name), encoding="utf-8")
    ensure_persistent_statuses(root)
    for name in QUEUE_FILES:
        p = root / "queues" / name
        if not p.exists():
            p.write_text("", encoding="utf-8")
    state = root / "orchestrator_state.json"
    if state.exists():
        data = json.loads(state.read_text(encoding="utf-8"))
        data.setdefault("profiles", [])
        data.setdefault("persistent_agents", DEFAULT_STATE["persistent_agents"])
        data.setdefault("wave_policy", DEFAULT_STATE["wave_policy"])
        data.setdefault("effort_policy", DEFAULT_STATE["effort_policy"])
        data.setdefault("integration_policy", DEFAULT_STATE["integration_policy"])
        data.setdefault("phase", "initialized")
        data.setdefault("active_wave", "Wave0")
        data.setdefault("active_gate", "Gate0")
        for profile in profiles:
            if profile not in data["profiles"]:
                data["profiles"].append(profile)
    else:
        data = dict(DEFAULT_STATE)
        data["created_at"] = now_iso()
        data["profiles"] = profiles
    state.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"initialized {root}")
    if profiles:
        print(f"profiles: {', '.join(profiles)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
