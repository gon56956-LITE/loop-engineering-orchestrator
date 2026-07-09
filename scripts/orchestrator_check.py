#!/usr/bin/env python3
import json
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

TERMINAL_STATES = {
    "accepted",
    "visual_accepted",
    "report_integrated",
    "gap",
    "declared_gap",
    "declared-gap",
    "subwave_closed",
    "released",
    "closed",
}
RECOVERY_STATES = {"suspended_by_transport", "resume_pending", "recovery_review"}
RELEASED_STATUSES = {"released", "closed", "carried_forward"}
FORBIDDEN_EFFORTS = {"low", "light"}
APPROVED_CUSTOM_AGENTS = {
    "handoff-steward",
    "evidence-analyst",
    "reviewer",
    "visual-producer",
    "visual-skill-maintainer",
}
OPTIONAL_CUSTOM_AGENTS = {
    "dependency-coordinator",
}
QUEUE_NAMES = [
    "dependency_requests.jsonl",
    "dependency_responses.jsonl",
    "specialist_requests.jsonl",
    "specialist_responses.jsonl",
    "re_requests.jsonl",
    "re_responses.jsonl",
    "review_queue.jsonl",
    "visual_queue.jsonl",
    "rework_queue.jsonl",
]

def parse_time(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

def age_minutes(dt, now):
    if not dt:
        return None
    return max(0.0, (now - dt).total_seconds() / 60.0)

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_error": str(exc)}

def jsonl_counts(path):
    counts = {}
    if not path.exists():
        return counts
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            status = obj.get("status", "unknown")
        except Exception:
            status = "invalid_json"
        counts[status] = counts.get(status, 0) + 1
    return counts

def newest_mtime(paths):
    newest = None
    for path in paths:
        if path.exists():
            m = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            newest = m if newest is None or m > newest else newest
    return newest

def inspect_custom_agents(state):
    policy = state.get("custom_agent_policy", {})
    approved = set(policy.get("approved_custom_agents", [])) or APPROVED_CUSTOM_AGENTS
    optional = set(policy.get("optional_custom_agents", [])) or OPTIONAL_CUSTOM_AGENTS
    all_known = approved | optional
    agent_dir = policy.get("authoritative_agent_dir", "~/.codex/agents")
    root = Path(agent_dir).expanduser()
    findings = {}
    for name in sorted(all_known):
        path = root / f"{name}.toml"
        if not path.exists():
            findings[name] = "missing_optional" if name in optional else "missing"
            continue
        try:
            data = path.read_bytes()
            if data.startswith(b"\xef\xbb\xbf"):
                findings[name] = "bom_present"
                continue
            parsed = tomllib.loads(data.decode("utf-8"))
            if parsed.get("name") != name:
                findings[name] = f"name_mismatch:{parsed.get('name')}"
            else:
                findings[name] = "ok"
        except Exception as exc:
            findings[name] = f"parse_error:{exc}"
    return approved, optional, findings

def fmt_age(value):
    return "unknown" if value is None else f"{value:.1f}"

def main():
    if len(sys.argv) != 2:
        print("usage: orchestrator_check.py <agent_work_dir>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    state = read_json(root / "orchestrator_state.json")
    heartbeat = float(state.get("heartbeat_minutes", 10))
    effort_policy = state.get("effort_policy", {})
    persistent_agents = state.get("persistent_agents", ["main-agent", "handoff-steward"])
    approved_custom_agents, optional_custom_agents, custom_agent_findings = inspect_custom_agents(state)
    known_custom_agents = approved_custom_agents | optional_custom_agents | {"main-agent"}
    now = datetime.now(timezone.utc)
    print("# Loop Orchestrator Dashboard")
    print(f"root: {root}")
    print(f"checked_at: {now.replace(microsecond=0).isoformat().replace('+00:00','Z')}")
    print(f"phase: {state.get('phase', '(not set)')}")
    print(f"active_wave: {state.get('active_wave', '(not set)')}")
    print(f"active_gate: {state.get('active_gate', '(not set)')}")
    print(f"profiles: {', '.join(state.get('profiles', [])) if state.get('profiles') else '(not set)'}")
    print(f"effort_strategy: {effort_policy.get('strategy', '(not set)')}")
    print("")
    print("## Agent Health")
    status_dir = root / "status"
    agents = sorted(status_dir.glob("*.json")) if status_dir.exists() else []
    if not agents:
        print("- no status files found")
    effort_counts = {}
    active_effort_counts = {}
    missing_effort = []
    forbidden_effort = []
    model_downgrade = []
    bad_persistent_lifecycle = []
    terminal_wave_agent_without_release = []
    unapproved_custom_agents = []
    active_optional_custom_agents = set()
    for path in agents:
        data = read_json(path)
        silent_until = parse_time(data.get("silent_window_until"))
        owned = []
        artifact = data.get("current_artifact")
        if artifact:
            ap = Path(artifact)
            owned.append(ap if ap.is_absolute() else (root.parent / ap))
        latest = newest_mtime([path] + owned)
        latest_age = age_minutes(latest, now)
        missed = int(latest_age // heartbeat) if latest_age is not None else 999
        state_name = data.get("state", "unknown")
        if state_name in TERMINAL_STATES:
            health = "terminal"
        elif state_name in RECOVERY_STATES:
            health = "recovery_pending"
        elif silent_until and silent_until > now:
            health = "quiet_expected"
        elif missed <= 1:
            health = "healthy"
        elif missed == 2:
            health = "needs_ping"
        elif missed == 3:
            health = "potentially_stuck"
        else:
            health = "intervene"
        role = data.get("role", "")
        profile = data.get("profile", "")
        effort = data.get("reasoning_effort", "unknown")
        effort_counts[effort] = effort_counts.get(effort, 0) + 1
        if state_name not in TERMINAL_STATES:
            active_effort_counts[effort] = active_effort_counts.get(effort, 0) + 1
        if effort == "unknown":
            missing_effort.append(path.stem)
        if str(effort).lower() in FORBIDDEN_EFFORTS:
            forbidden_effort.append(path.stem)
        model_policy = str(data.get("model_policy", "")).lower()
        if data.get("model_downgrade") is True or "downgrade" in model_policy and "no_downgrade" not in model_policy:
            model_downgrade.append(path.stem)
        if path.stem in persistent_agents and data.get("lifecycle") != "persistent":
            bad_persistent_lifecycle.append(path.stem)
        custom_agent = data.get("custom_agent", "")
        if custom_agent in optional_custom_agents:
            active_optional_custom_agents.add(custom_agent)
        if custom_agent and custom_agent not in known_custom_agents:
            unapproved_custom_agents.append(f"{path.stem}:{custom_agent}")
        lifecycle = data.get("lifecycle", "")
        wave_id = data.get("wave_id", "")
        subwave_id = data.get("subwave_id", "")
        release_status = data.get("release_status", "")
        if lifecycle == "wave_scoped" and state_name in TERMINAL_STATES:
            if str(release_status).lower() not in RELEASED_STATUSES:
                terminal_wave_agent_without_release.append(path.stem)
        print(f"- {path.stem}: health={health}; state={state_name}; role={role}; custom_agent={custom_agent}; lifecycle={lifecycle}; wave={wave_id}; subwave={subwave_id}; release={release_status}; profile={profile}; effort={effort}; latest_age_min={fmt_age(latest_age)}; next={data.get('next_step','')}")
    print("")
    print("## Custom Agent Configs")
    for name, result in custom_agent_findings.items():
        print(f"- {name}: {result}")
    print("")
    print("## Reasoning Effort")
    if effort_counts:
        print(f"- all_agents: {effort_counts}")
        print(f"- active_agents: {active_effort_counts if active_effort_counts else '{}'}")
    else:
        print("- no effort data found")
    print("")
    print("## Queue Counts")
    any_counts = False
    for name in QUEUE_NAMES:
        counts = jsonl_counts(root / "queues" / name)
        if counts:
            any_counts = True
            print(f"- {name}: {counts}")
    if not any_counts:
        print("- all queues empty")
    print("")
    print("## Basic Gate Warnings")
    warnings = []
    required_controls = [
        "agent_roster.md",
        "orchestration_plan.md",
        "wave_register.md",
        "source_manifest.md",
        "claim_trace_matrix.md",
        "dependency_graph.md",
        "dependency_conflicts.md",
        "risk_register.md",
        "recovery_log.md",
        "subwave_closeout_log.md",
        "gate_log.md",
        "integration_plan.md",
        "review_log.md",
        "handoff.md",
        "orchestrator_state.json",
    ]
    for required in required_controls:
        if not (root / required).exists():
            warnings.append(f"missing_control_file: {required}")
    for agent_id in persistent_agents:
        if not (root / "status" / f"{agent_id}.json").exists():
            warnings.append(f"missing_persistent_agent_status: {agent_id}")
    if missing_effort:
        warnings.append(f"missing_reasoning_effort: {', '.join(missing_effort)}")
    if forbidden_effort:
        warnings.append(f"forbidden_low_or_light_effort: {', '.join(forbidden_effort)}")
    if model_downgrade:
        warnings.append(f"model_downgrade_detected: {', '.join(model_downgrade)}")
    if bad_persistent_lifecycle:
        warnings.append(f"persistent_agent_wrong_lifecycle: {', '.join(bad_persistent_lifecycle)}")
    if terminal_wave_agent_without_release:
        warnings.append(f"terminal_wave_agent_without_release_status: {', '.join(terminal_wave_agent_without_release)}")
    missing_or_invalid_custom_agents = []
    for name, result in custom_agent_findings.items():
        if result == "ok":
            continue
        if result == "missing_optional" and name not in active_optional_custom_agents:
            continue
        missing_or_invalid_custom_agents.append(f"{name}:{result}")
    if missing_or_invalid_custom_agents:
        warnings.append(f"custom_agent_config_not_ready: {', '.join(missing_or_invalid_custom_agents)}")
    if unapproved_custom_agents:
        warnings.append(f"unapproved_custom_agent_in_status: {', '.join(unapproved_custom_agents)}")
    dependency_request_counts = jsonl_counts(root / "queues" / "dependency_requests.jsonl")
    active_dependency_requests = sum(
        count for status, count in dependency_request_counts.items()
        if status not in TERMINAL_STATES and status not in {"answered", "closed", "resolved", "cancelled", "canceled"}
    )
    dependency_coordinator_active = "dependency-coordinator" in active_optional_custom_agents
    if active_dependency_requests and not dependency_coordinator_active:
        warnings.append(f"active_dependency_requests_without_coordinator: {active_dependency_requests}")
    if dependency_coordinator_active and custom_agent_findings.get("dependency-coordinator") != "ok":
        warnings.append(f"dependency_coordinator_config_not_ready: {custom_agent_findings.get('dependency-coordinator', 'missing')}")
    if active_dependency_requests and not (root / "dependency_graph.md").exists():
        warnings.append("active_dependency_requests_missing_dependency_graph")
    if any((root / "shared_contracts").glob("*.md")) if (root / "shared_contracts").exists() else False:
        if not (root / "dependency_graph.md").exists():
            warnings.append("shared_contracts_missing_dependency_graph")
    for folder in ["workflows", "figures", "semantic"]:
        candidate = root.parent / folder
        if candidate.exists():
            for svg in candidate.glob("*.svg"):
                if svg.stat().st_size < 100:
                    warnings.append(f"small_svg: {svg}")
                if not svg.with_suffix(".json").exists():
                    warnings.append(f"missing_json_for_svg: {svg}")
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- no basic warnings found")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
