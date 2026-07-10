#!/usr/bin/env python3
import argparse
import json
import os
import sys
import tomllib
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
BUNDLE_DIR = SKILL_ROOT / "custom-agents"
MANIFEST_PATH = BUNDLE_DIR / "manifest.json"


def resolve_codex_home(explicit):
    if explicit:
        return Path(explicit).expanduser().resolve()
    configured = os.environ.get("CODEX_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def load_manifest():
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    roles = data.get("roles", [])
    if not isinstance(roles, list) or not roles:
        raise ValueError("custom-agents/manifest.json has no roles")
    return roles


def validate_toml(path, expected_name):
    try:
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            return "bom_present"
        parsed = tomllib.loads(raw.decode("utf-8"))
    except Exception as exc:
        return f"parse_error:{exc}"
    actual_name = parsed.get("name")
    if actual_name != expected_name:
        return f"name_mismatch:{actual_name}"
    return "ok"


def check_roles(roles, destination):
    results = []
    for role in roles:
        name = role["name"]
        path = destination / f"{name}.toml"
        result = validate_toml(path, name) if path.exists() else "missing"
        results.append((role, path, result))
    return results


def print_check(results):
    for role, path, result in results:
        print(
            f"{role['name']}: {result}; requirement={role['requirement']}; "
            f"lifecycle={role['lifecycle']}; path={path}"
        )


def check_exit_code(results):
    blocking = [
        role["name"]
        for role, _, result in results
        if role["requirement"] == "base_required" and result != "ok"
    ]
    if blocking:
        print(f"blocking base roles: {', '.join(blocking)}", file=sys.stderr)
        return 1
    return 0


def install_roles(roles, destination, force, dry_run):
    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)
    conflicts = []
    for role in roles:
        name = role["name"]
        source = BUNDLE_DIR / f"{name}.toml"
        target = destination / source.name
        source_status = validate_toml(source, name)
        if source_status != "ok":
            raise ValueError(f"bundled role {name} is invalid: {source_status}")
        source_bytes = source.read_bytes()
        if target.exists():
            if target.read_bytes() == source_bytes:
                print(f"{name}: already current")
                continue
            if not force:
                conflicts.append(name)
                print(f"{name}: conflict, kept existing file at {target}")
                continue
            action = "would overwrite" if dry_run else "overwritten"
        else:
            action = "would install" if dry_run else "installed"
        if not dry_run:
            target.write_bytes(source_bytes)
        print(f"{name}: {action} at {target}")
    if conflicts:
        print(
            "conflicts require manual review or an explicit --force: "
            + ", ".join(conflicts),
            file=sys.stderr,
        )
        return 1
    return 0


def parse_args():
    parser = argparse.ArgumentParser(
        description="Install or check loop-engineering-orchestrator custom agents."
    )
    parser.add_argument(
        "--codex-home",
        help="Override CODEX_HOME. Defaults to $CODEX_HOME or ~/.codex.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check installed role definitions without writing files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show install actions without writing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite different same-name role files.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    roles = load_manifest()
    destination = resolve_codex_home(args.codex_home) / "agents"
    if args.check:
        results = check_roles(roles, destination)
        print_check(results)
        return check_exit_code(results)
    return install_roles(roles, destination, args.force, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
