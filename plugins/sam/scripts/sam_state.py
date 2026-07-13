#!/usr/bin/env python3
"""State, validation, migration, and scaffolding helper for the SAM plugin."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path


DOC_ROOT = Path("docs") / "architecture"
LEGACY_DOC_ROOT = Path("docs") / "arquitecture"
DELIVERY_ROOT = DOC_ROOT / "delivery"
LEGACY_DELIVERY_ROOT = DOC_ROOT / "04-architectural-implementation"
STATE_PATH = DOC_ROOT / ".sam" / "state.json"
INDEX_PATH = DOC_ROOT / "README.md"
AGENTS_PATH = Path("AGENTS.md")

SCRIPT_ROOT = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPT_ROOT.parent
SKILL_ROOT = PLUGIN_ROOT / "skills" / "sam"
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "templates"

AGENTS_START = "<!-- SAM:ARCHITECTURE:START -->"
AGENTS_END = "<!-- SAM:ARCHITECTURE:END -->"

CORE_GATE_ORDER = ["brief", "phase-1-drivers", "phase-2-design", "phase-3-document"]
NEXT_GATE = {
    "brief": "phase-1-drivers",
    "phase-1-drivers": "phase-2-design",
    "phase-2-design": "phase-3-document",
    "phase-3-document": "complete",
}

ARTIFACTS = {
    "project-brief": DOC_ROOT / "project-brief.md",
    "phase-1-input": DOC_ROOT / "01-architectural-requirements" / "input.md",
    "phase-1-drivers": DOC_ROOT / "01-architectural-requirements" / "architecture-drivers.md",
    "phase-2-input": DOC_ROOT / "02-architectural-design" / "input.md",
    "phase-2-iteration-plan": DOC_ROOT / "02-architectural-design" / "iteration-plan.md",
    "phase-2-decisions": DOC_ROOT / "02-architectural-design" / "design-decisions.md",
    "phase-3-input": DOC_ROOT / "03-architectural-documentation" / "input.md",
    "phase-3-document": DOC_ROOT / "03-architectural-documentation" / "architecture-document.md",
    "delivery-input": DELIVERY_ROOT / "input.md",
    "delivery-plan": DELIVERY_ROOT / "implementation-plan.md",
    "delivery-design-system": DELIVERY_ROOT / "design-system.md",
}

GATES = {
    "brief": ["project-brief"],
    "phase-1-drivers": ["phase-1-drivers"],
    "phase-2-design": ["phase-2-iteration-plan", "phase-2-decisions"],
    "phase-3-document": ["phase-3-document"],
    "delivery": ["delivery-plan"],
    "design-system": ["delivery-design-system"],
}

DEPENDENCIES = {
    "phase-1-input": ["project-brief"],
    "phase-1-drivers": ["project-brief", "phase-1-input"],
    "phase-2-input": ["phase-1-drivers"],
    "phase-2-iteration-plan": ["phase-1-drivers", "phase-2-input"],
    "phase-2-decisions": ["phase-1-drivers", "phase-2-input", "phase-2-iteration-plan"],
    "phase-3-input": ["phase-2-iteration-plan", "phase-2-decisions"],
    "phase-3-document": ["phase-2-iteration-plan", "phase-2-decisions", "phase-3-input"],
    "delivery-input": ["phase-3-document"],
    "delivery-plan": ["phase-3-document", "phase-2-decisions", "delivery-input"],
    "delivery-design-system": ["phase-3-document", "delivery-input"],
}

REQUIRED_SECTIONS = {
    "project-brief": [
        "Business Problem", "System Goal", "Initial Scope / MVP", "Stakeholders",
        "Main Features", "Expected Quality Attributes", "Constraints", "Current Context",
        "Environments And Operations", "Customer Priorities", "Risk, Rigor And System Context",
        "Data, Security And Recovery", "Assumptions And Open Questions",
    ],
    "phase-1-drivers": [
        "Intake Summary", "ASR Classification", "Quality Attribute Scenarios",
        "Assumptions And Concerns", "Utility Tree", "Driver Proposal",
        "Open Questions And Risks", "Exit Checklist",
    ],
    "phase-2-iteration-plan": ["Design Context", "Iteration Plan", "Execution Record", "Exit Checklist"],
    "phase-2-decisions": [
        "Selected Concepts And Tradeoffs", "Instantiated Elements And Interfaces",
        "Architectural Decisions", "Provisional Views", "Driver Coverage And Evidence Plan",
        "Risks And Follow-Up", "Exit Checklist",
    ],
    "phase-3-document": [
        "Purpose, Audiences And Uses", "System Context And Scope",
        "Architectural Drivers And Scenarios", "View Selection", "Architecture Views",
        "Architectural Decisions", "Interfaces And Runtime Behavior",
        "Quality, Security, Data And Operations", "Traceability And Evidence",
        "Risks, Assumptions And Technical Debt", "Governance And Agent Guidance", "Exit Checklist",
    ],
    "delivery-plan": [
        "Authoritative Sources", "Delivery And Technology Constraints", "Implementation Order",
        "Implementation Slices", "Code Agent Prompt", "Slice Governance And Evidence", "Exit Checklist",
    ],
}

TEMPLATE_PARITY = {
    "project-brief.md": Path("project-brief-template.md"),
    "architecture-drivers.md": Path("01-architectural-requirements") / "template.md",
    "iteration-plan.md": Path("02-architectural-design") / "iteration-plan-template.md",
    "design-decisions.md": Path("02-architectural-design") / "design-decisions-template.md",
    "architecture-document.md": Path("03-architectural-documentation") / "template.md",
    "implementation-plan.md": Path("delivery") / "template.md",
    "design-system.md": Path("delivery") / "design-system-template.md",
}

SCAFFOLD_MARKERS = ["|  |", "@ pending", "SLICE-NNN", "CHECK-NNN", "<Project>", "[TODO:"]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def fail(message: str, code: int = 2) -> None:
    print(message)
    raise SystemExit(code)


def content_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def migrate_legacy_paths() -> None:
    if LEGACY_DOC_ROOT.exists() and not DOC_ROOT.exists():
        DOC_ROOT.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(LEGACY_DOC_ROOT), str(DOC_ROOT))
        print(f"Migrated legacy SAM workspace from {LEGACY_DOC_ROOT} to {DOC_ROOT}")
    elif LEGACY_DOC_ROOT.exists() and DOC_ROOT.exists():
        fail(f"Both {DOC_ROOT} and {LEGACY_DOC_ROOT} exist; reconcile them manually.")

    if LEGACY_DELIVERY_ROOT.exists() and not DELIVERY_ROOT.exists():
        shutil.move(str(LEGACY_DELIVERY_ROOT), str(DELIVERY_ROOT))
        print(f"Migrated legacy delivery handoff from {LEGACY_DELIVERY_ROOT} to {DELIVERY_ROOT}")
    elif LEGACY_DELIVERY_ROOT.exists() and DELIVERY_ROOT.exists():
        fail(f"Both {DELIVERY_ROOT} and {LEGACY_DELIVERY_ROOT} exist; reconcile them manually.")


def default_state(project_name: str = "Project") -> dict:
    return {
        "version": 3,
        "projectName": project_name,
        "currentGate": "brief",
        "artifacts": {},
        "approvals": [],
        "delivery": {"status": "not-started"},
    }


def migrate_state_v2(state: dict) -> tuple[dict, bool]:
    if state.get("version", 2) >= 3:
        return state, False

    key_map = {
        "phase-4-input": "delivery-input",
        "phase-4-implementation-plan": "delivery-plan",
        "phase-4-design-system": "delivery-design-system",
    }
    migrated = default_state(state.get("projectName", "Project"))
    migrated["approvals"] = state.get("approvals", [])
    migrated["reopenings"] = state.get("reopenings", [])
    migrated["currentGate"] = state.get("currentGate", "brief")
    if migrated["currentGate"] == "phase-4-implementation":
        migrated["currentGate"] = "complete"
        migrated["delivery"]["status"] = "draft"

    for old_key, record in state.get("artifacts", {}).items():
        new_key = key_map.get(old_key, old_key)
        updated = dict(record)
        if new_key in ARTIFACTS:
            updated["path"] = str(ARTIFACTS[new_key])
        migrated["artifacts"][new_key] = updated
        if new_key == "delivery-plan":
            migrated["delivery"]["status"] = updated.get("status", "draft")

    for approval in migrated["approvals"]:
        if approval.get("gate") == "phase-4-implementation":
            approval["gate"] = "delivery"
            migrated["delivery"]["status"] = "approved"
    return migrated, True


def load_state() -> dict:
    migrate_legacy_paths()
    if not STATE_PATH.exists():
        return default_state()
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    state, changed = migrate_state_v2(state)
    if changed:
        save_state(state)
        print("Migrated SAM state to version 3")
    return state


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def write_once(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def replace_first_heading(text: str, heading: str) -> str:
    return re.sub(r"(?m)^# .+$", f"# {heading}", text, count=1)


def render_asset(filename: str, heading: str) -> str:
    path = TEMPLATE_ROOT / filename
    if not path.exists():
        fail(f"Missing SAM template asset: {path}")
    return replace_first_heading(path.read_text(encoding="utf-8"), heading)


def blank_brief(name: str) -> str:
    sections = "\n\n".join(f"## {index}. {section}\n" for index, section in enumerate(REQUIRED_SECTIONS["project-brief"], 1))
    return f"# {name} - Project Brief\n\n{sections}\n"


def phase_input_template(title: str, source_key: str | None) -> str:
    source = "- None (initial phase input)" if source_key is None else f"- `{ARTIFACTS[source_key]}` @ pending"
    return f"""# {title}

Status: Draft
Generated by: SAM agent
Approved by:
Approved date:
Rigor profile: Lite / Standard / High Assurance
System context: Greenfield / Evolution / Integration
Source artifacts:
{source}

## Input Delta

Record only phase-specific clarifications, architect corrections, accepted assumptions, or constraints not already present in approved sources.

- Add phase-specific information here.
"""


def replace_metadata(text: str, field: str, value: str) -> str:
    pattern = rf"(?m)^{re.escape(field)}:.*$"
    replacement = f"{field}: {value}"
    if re.search(pattern, text):
        return re.sub(pattern, replacement, text, count=1)
    lines = text.splitlines()
    lines.insert(1 if lines else 0, replacement)
    return "\n".join(lines) + "\n"


def sync_markdown_status(path: Path, status_value: str, approved_by: str = "", approved_at: str = "") -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_metadata(text, "Status", status_value)
    if approved_by:
        text = replace_metadata(text, "Approved by", approved_by)
    if approved_at:
        text = replace_metadata(text, "Approved date", approved_at)
    path.write_text(text, encoding="utf-8")


def sync_source_hashes(key: str) -> None:
    dependencies = DEPENDENCIES.get(key, [])
    if not dependencies or not ARTIFACTS[key].exists():
        return
    missing = [dependency for dependency in dependencies if not ARTIFACTS[dependency].exists()]
    if missing:
        fail(f"Cannot sync sources for {key}; missing: {', '.join(missing)}")
    lines = "".join(f"- `{ARTIFACTS[dependency]}` @ {content_hash(ARTIFACTS[dependency])}\n" for dependency in dependencies)
    text = ARTIFACTS[key].read_text(encoding="utf-8")
    pattern = r"(?m)^Source artifacts:\n(?:- [^\n]*\n)*"
    replacement = f"Source artifacts:\n{lines}"
    if re.search(pattern, text):
        text = re.sub(pattern, replacement, text, count=1)
    else:
        heading = re.search(r"(?m)^## ", text)
        insert_at = heading.start() if heading else len(text)
        text = text[:insert_at] + replacement + "\n" + text[insert_at:]
    ARTIFACTS[key].write_text(text, encoding="utf-8")


def write_agents_block() -> None:
    block = f"""{AGENTS_START}
## SAM Architecture Memory

Before planning or changing code, read `docs/architecture/README.md` and the approved artifacts it identifies. Approved drivers and ADRs are implementation constraints; Draft and In Review artifacts are proposals only. Do not silently contradict an approved decision. If an approved source changed or the code requires a different architecture, run the SAM reopen workflow and review dependent artifacts.
{AGENTS_END}"""
    current = AGENTS_PATH.read_text(encoding="utf-8") if AGENTS_PATH.exists() else ""
    pattern = rf"(?ms){re.escape(AGENTS_START)}.*?{re.escape(AGENTS_END)}"
    if re.search(pattern, current):
        updated = re.sub(pattern, block, current, count=1)
    else:
        separator = "\n\n" if current.strip() else ""
        updated = current.rstrip() + separator + block + "\n"
    AGENTS_PATH.write_text(updated, encoding="utf-8")


def recorded_status(state: dict, key: str) -> str:
    return state.get("artifacts", {}).get(key, {}).get("status", "missing")


def artifact_status(state: dict, key: str) -> str:
    path = ARTIFACTS[key]
    if not path.exists():
        return "missing"
    record = state.get("artifacts", {}).get(key, {})
    status = record.get("status", "draft")
    if status == "approved" and record.get("hash") and record["hash"] != content_hash(path):
        return "drift"
    if status == "approved" and DEPENDENCIES.get(key):
        text = path.read_text(encoding="utf-8")
        if validate_sources(key, text):
            return "drift"
    return status


def write_index(state: dict) -> None:
    DOC_ROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    for key in [
        "project-brief", "phase-1-drivers", "phase-2-iteration-plan",
        "phase-2-decisions", "phase-3-document", "delivery-plan", "delivery-design-system",
    ]:
        path = ARTIFACTS[key]
        rows.append(f"| `{key}` | {artifact_status(state, key)} | `{path}` |")
    content = f"""# SAM Architecture Memory

Generated by the SAM state helper. Do not edit this index manually; edit the linked artifacts.

Current core gate: **{state.get('currentGate', 'brief')}**
Optional delivery status: **{state.get('delivery', {}).get('status', 'not-started')}**

## Authority Rules

- Approved artifacts are authoritative architecture guidance.
- Draft and In Review artifacts are proposals.
- Superseded or drifted artifacts must not guide new implementation.
- Reopen a gate before changing an approved driver or decision.

## Artifact Status

| Artifact | Status | Path |
| --- | --- | --- |
{chr(10).join(rows)}

## Agent Reading Order

1. Read this index and check for drift or superseded sources.
2. Read the approved `architecture-document.md` when it exists.
3. Read the approved drivers and design decisions relevant to the task.
4. For implementation, read only an approved delivery slice and its referenced CHECK definitions.
5. Stop and request a SAM reopen when the requested work contradicts approved architecture.
"""
    INDEX_PATH.write_text(content, encoding="utf-8")


def section_body(text: str, section: str) -> str:
    match = re.search(rf"(?m)^##+\s+(?:\d+\.\s+)?{re.escape(section)}\s*$", text)
    if not match:
        return ""
    rest = text[match.end():]
    next_heading = re.search(r"(?m)^##\s+", rest)
    body = rest[:next_heading.start()] if next_heading else rest
    return body.strip()


def source_hashes(text: str) -> dict[str, str]:
    result = {}
    for path, digest in re.findall(r"(?m)^- `?([^`\n]+?)`? @ ([A-Za-z0-9._-]+)\s*$", text):
        result[path.strip()] = digest
    return result


def ids_in_section(text: str, section: str, prefix: str) -> list[str]:
    body = section_body(text, section)
    return re.findall(rf"(?m)^\|\s*({prefix}-\d{{3}})\s*\|", body)


def primary_drivers() -> list[str]:
    path = ARTIFACTS["phase-1-drivers"]
    if not path.exists():
        return []
    body = section_body(path.read_text(encoding="utf-8"), "Driver Proposal")
    drivers = []
    for line in body.splitlines():
        match = re.match(r"^\|\s*(DRV-\d{3})\s*\|", line)
        if match and re.search(r"\|\s*Primary\s*\|", line, re.IGNORECASE):
            drivers.append(match.group(1))
    if not drivers:
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^\|\s*(DRV-\d{3})\s*\|", line)
            if match and re.search(r"\|\s*Primary\s*\|", line, re.IGNORECASE):
                drivers.append(match.group(1))
    return sorted(set(drivers))


def line_for_id(body: str, identifier: str) -> str:
    for line in body.splitlines():
        if re.search(rf"\b{re.escape(identifier)}\b", line):
            return line
    return ""


def validate_sources(key: str, text: str) -> list[str]:
    errors = []
    expected = DEPENDENCIES.get(key, [])
    if not expected:
        return errors
    recorded = source_hashes(text)
    for dependency in expected:
        path = ARTIFACTS[dependency]
        if not path.exists():
            errors.append(f"source artifact is missing: {path}")
            continue
        digest = recorded.get(str(path))
        if digest is None:
            errors.append(f"source hash is missing: {path}")
        elif digest != content_hash(path):
            errors.append(f"source hash is stale: {path}")
    return errors


def validate_verified_evidence(text: str) -> list[str]:
    errors = []
    for line in text.splitlines():
        if "|" in line and re.search(r"\bVerified\b", line) and not re.search(r"Pending / Verified", line):
            if "Evidence:" not in line or "Executed:" not in line:
                errors.append("Verified requires Evidence: and Executed: metadata in the same trace row")
                break
    return errors


def validate_artifact(key: str) -> list[str]:
    path = ARTIFACTS[key]
    if not path.exists():
        return ["artifact is missing"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if len(text.strip()) < 80:
        errors.append("artifact is empty or only a stub")
    for section in REQUIRED_SECTIONS.get(key, []):
        if not section_body(text, section):
            errors.append(f"missing or empty section: {section}")

    if key == "project-brief":
        for section in REQUIRED_SECTIONS[key]:
            body = re.sub(r"<!--.*?-->", "", section_body(text, section), flags=re.S).strip()
            if len(re.findall(r"[A-Za-z0-9]+", body)) < 3:
                errors.append(f"brief section has no meaningful content: {section}")
        return errors

    for field in ["Status", "Generated by", "Approved by", "Approved date", "Source artifacts"]:
        if not re.search(rf"(?m)^{re.escape(field)}:", text):
            errors.append(f"missing metadata: {field}")
    if not re.search(r"(?m)^Rigor profile: (?:Lite|Standard|High Assurance)$", text):
        errors.append("missing or invalid rigor profile")
    if not re.search(r"(?m)^System context: (?:Greenfield|Evolution|Integration)$", text):
        errors.append("missing or invalid system context")
    errors.extend(validate_sources(key, text))

    unchecked = re.findall(r"(?m)^- \[ \] (.+)$", text)
    if unchecked:
        errors.append("exit checklist contains unchecked items")
    if "Exit Checklist" in REQUIRED_SECTIONS.get(key, []) and not re.search(r"(?m)^- \[x\]", text):
        errors.append("exit checklist has no completed items")
    for marker in SCAFFOLD_MARKERS:
        if marker in text:
            errors.append(f"unresolved scaffold marker: {marker}")
    errors.extend(validate_verified_evidence(text))

    if key == "phase-1-drivers":
        for section, prefix in [("ASR Classification", "REQ"), ("Quality Attribute Scenarios", "QA"), ("Driver Proposal", "DRV")]:
            ids = ids_in_section(text, section, prefix)
            if len(ids) != len(set(ids)):
                errors.append(f"duplicate {prefix} ID in {section}")
        if not primary_drivers():
            body = section_body(text, "Driver Proposal")
            if "no primary driver" not in body.lower():
                errors.append("no primary driver or explicit no-primary-driver rationale")

    if key == "phase-2-decisions":
        defined_adrs = set(ids_in_section(text, "Architectural Decisions", "ADR"))
        if len(defined_adrs) != len(ids_in_section(text, "Architectural Decisions", "ADR")):
            errors.append("duplicate ADR ID")
        coverage = section_body(text, "Driver Coverage And Evidence Plan")
        known_drivers = set(re.findall(r"\bDRV-\d{3}\b", ARTIFACTS["phase-1-drivers"].read_text(encoding="utf-8")))
        referenced_drivers = set(re.findall(r"\bDRV-\d{3}\b", text))
        unknown = referenced_drivers - known_drivers
        if unknown:
            errors.append("unknown driver reference(s): " + ", ".join(sorted(unknown)))
        for driver in primary_drivers():
            line = line_for_id(coverage, driver)
            if not line:
                errors.append(f"primary driver missing from coverage: {driver}")
            elif not re.search(r"\bCHECK-\d{3}\b", line):
                errors.append(f"primary driver has no CHECK: {driver}")
            elif not re.search(r"\bADR-\d{3}\b|Accepted Risk", line, re.IGNORECASE):
                errors.append(f"primary driver has no ADR or accepted risk: {driver}")
        if not defined_adrs and "no material adr" not in section_body(text, "Architectural Decisions").lower():
            errors.append("no ADR definitions or explicit no-material-ADR rationale")

    if key == "phase-3-document":
        trace = section_body(text, "Traceability And Evidence")
        for driver in primary_drivers():
            line = line_for_id(trace, driver)
            if not line:
                errors.append(f"primary driver missing from traceability: {driver}")
            elif not re.search(r"\bCHECK-\d{3}\b", line):
                errors.append(f"primary driver has no traceability CHECK: {driver}")
            elif not re.search(r"\bADR-\d{3}\b|Accepted Risk", line, re.IGNORECASE):
                errors.append(f"primary driver has no traced ADR or accepted risk: {driver}")

    if key == "delivery-plan":
        slice_ids = re.findall(r"(?m)^###\s+(SLICE-\d{3})\b", text)
        if not slice_ids:
            errors.append("delivery plan has no implementation slice")
        if len(slice_ids) != len(set(slice_ids)):
            errors.append("duplicate SLICE ID")
        governance = section_body(text, "Slice Governance And Evidence")
        for driver in primary_drivers():
            line = line_for_id(governance, driver)
            if not line or not re.search(r"\bSLICE-\d{3}\b", line) or not re.search(r"\bCHECK-\d{3}\b", line):
                errors.append(f"primary driver lacks slice/check delivery trace: {driver}")

    return sorted(set(errors))


def init(args: argparse.Namespace) -> None:
    migrate_legacy_paths()
    name = args.name.strip() or "Project"
    for directory in [
        DOC_ROOT / "01-architectural-requirements",
        DOC_ROOT / "02-architectural-design",
        DOC_ROOT / "03-architectural-documentation",
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    write_once(ARTIFACTS["project-brief"], blank_brief(name))
    write_once(ARTIFACTS["phase-1-input"], phase_input_template("Phase 1 - Architectural Requirements Input", "project-brief"))
    write_once(ARTIFACTS["phase-1-drivers"], render_asset("architecture-drivers.md", f"{name} - Architectural Requirements"))
    write_once(ARTIFACTS["phase-2-input"], phase_input_template("Phase 2 - Architectural Design Input", "phase-1-drivers"))
    write_once(ARTIFACTS["phase-2-iteration-plan"], render_asset("iteration-plan.md", f"{name} - ADD Iteration Plan"))
    write_once(ARTIFACTS["phase-2-decisions"], render_asset("design-decisions.md", f"{name} - ADD Design Decisions"))
    write_once(ARTIFACTS["phase-3-input"], phase_input_template("Phase 3 - Architectural Documentation Input", "phase-2-decisions"))
    write_once(ARTIFACTS["phase-3-document"], render_asset("architecture-document.md", f"{name} - Architecture Document"))

    state = load_state()
    state["projectName"] = name
    for key in [
        "project-brief", "phase-1-input", "phase-1-drivers", "phase-2-input",
        "phase-2-iteration-plan", "phase-2-decisions", "phase-3-input", "phase-3-document",
    ]:
        state["artifacts"].setdefault(key, {"path": str(ARTIFACTS[key]), "status": "draft"})
    save_state(state)
    write_agents_block()
    write_index(state)
    print(f"Initialized three-phase SAM workspace at {DOC_ROOT}")


def init_delivery(state: dict) -> None:
    require_approved(state, ["phase-3-document"], "handoff")
    DELIVERY_ROOT.mkdir(parents=True, exist_ok=True)
    name = state.get("projectName", "Project")
    write_once(ARTIFACTS["delivery-input"], phase_input_template("Optional Delivery Handoff Input", "phase-3-document"))
    write_once(ARTIFACTS["delivery-plan"], render_asset("implementation-plan.md", f"{name} - Delivery Implementation Plan"))
    for key in ["delivery-input", "delivery-plan"]:
        state["artifacts"].setdefault(key, {"path": str(ARTIFACTS[key]), "status": "draft"})
    state["delivery"]["status"] = "draft"
    save_state(state)
    write_index(state)


def mark_draft(args: argparse.Namespace) -> None:
    if args.artifact not in ARTIFACTS:
        fail(f"Unknown artifact: {args.artifact}")
    path = ARTIFACTS[args.artifact]
    if not path.exists():
        fail(f"Cannot mark missing artifact as draft: {path}")
    state = load_state()
    if artifact_status(state, args.artifact) == "approved":
        fail(f"Cannot silently modify approved artifact {args.artifact}; reopen its gate first.")
    if args.artifact != "project-brief":
        sync_source_hashes(args.artifact)
        sync_markdown_status(path, "Draft")
    state["artifacts"][args.artifact] = {"path": str(path), "status": "draft", "hash": content_hash(path)}
    if args.artifact.startswith("delivery-"):
        state["delivery"]["status"] = "draft"
    save_state(state)
    write_index(state)
    print(f"Marked draft and synchronized sources: {args.artifact}")


def require_approved(state: dict, keys: list[str], step: str) -> None:
    blocked = [key for key in keys if artifact_status(state, key) != "approved"]
    if blocked:
        fail(f"{step} is blocked. Current approved source required for: {', '.join(blocked)}")


def approve(args: argparse.Namespace) -> None:
    if args.gate not in GATES:
        fail(f"Unknown gate: {args.gate}")
    state = load_state()

    if args.gate in CORE_GATE_ORDER and state.get("currentGate", "brief") != args.gate:
        fail(f"Cannot approve {args.gate}; current core gate is {state.get('currentGate', 'brief')}")
    if args.gate == "delivery":
        require_approved(state, ["phase-3-document"], "delivery approval")
    if args.gate == "design-system":
        require_approved(state, ["phase-3-document"], "design-system approval")

    missing = [key for key in GATES[args.gate] if not ARTIFACTS[key].exists()]
    if missing:
        fail("Cannot approve missing artifact(s): " + ", ".join(missing))
    validation_errors = {key: validate_artifact(key) for key in GATES[args.gate]}
    validation_errors = {key: errors for key, errors in validation_errors.items() if errors}
    if validation_errors:
        details = "; ".join(f"{key}: {', '.join(errors)}" for key, errors in validation_errors.items())
        fail(f"Cannot approve invalid artifact(s): {details}")

    approved_at = now_iso()
    for key in GATES[args.gate]:
        if key != "project-brief":
            if key == "delivery-design-system":
                text = ARTIFACTS[key].read_text(encoding="utf-8")
                text = replace_metadata(text, "Status", "Approved")
                text = replace_metadata(text, "Product/design approved by", args.approved_by)
                text = replace_metadata(text, "Product/design approved date", approved_at)
                ARTIFACTS[key].write_text(text, encoding="utf-8")
            else:
                sync_markdown_status(ARTIFACTS[key], "Approved", args.approved_by, approved_at)
    for key in GATES[args.gate]:
        sync_source_hashes(key)
    for key in GATES[args.gate]:
        state["artifacts"][key] = {
            "path": str(ARTIFACTS[key]), "status": "approved", "hash": content_hash(ARTIFACTS[key])
        }

    state["approvals"].append({
        "gate": args.gate,
        "approvedBy": args.approved_by,
        "approvedAt": approved_at,
        "sourceVersions": {key: content_hash(path) for key, path in ARTIFACTS.items() if path.exists()},
    })
    if args.gate in NEXT_GATE:
        state["currentGate"] = NEXT_GATE[args.gate]
    elif args.gate == "delivery":
        state["delivery"]["status"] = "approved"
    save_state(state)
    write_index(state)
    print(f"Approved {args.gate}; current core gate is {state['currentGate']}")


def can_run(args: argparse.Namespace) -> None:
    state = load_state()
    step = "handoff" if args.step == "step-four" else args.step
    requirements = {
        "step-one": ["project-brief"],
        "step-two": ["phase-1-drivers"],
        "step-three": ["phase-2-iteration-plan", "phase-2-decisions"],
        "handoff": ["phase-3-document"],
        "slice": ["delivery-plan"],
    }
    if step not in requirements:
        fail(f"Unknown step: {args.step}")
    require_approved(state, requirements[step], step)
    if args.step == "step-four":
        print("DEPRECATED: step-four is now the optional @sam handoff workflow.")
    print(f"OK: {step} is unblocked")


def next_action(state: dict) -> str:
    drift = [key for key in ARTIFACTS if artifact_status(state, key) == "drift"]
    if drift:
        return "Approved-source drift detected in " + ", ".join(drift) + ". Reopen the earliest affected gate."
    if not ARTIFACTS["project-brief"].exists():
        return "Run @sam init."
    gate = state.get("currentGate", "brief")
    gate_steps = {
        "brief": (["project-brief"], None),
        "phase-1-drivers": (["phase-1-drivers"], "@sam step-one"),
        "phase-2-design": (["phase-2-iteration-plan", "phase-2-decisions"], "@sam step-two"),
        "phase-3-document": (["phase-3-document"], "@sam step-three"),
    }
    if gate in gate_steps:
        keys, command = gate_steps[gate]
        errors = {key: validate_artifact(key) for key in keys}
        errors = {key: value for key, value in errors.items() if value}
        if errors:
            if command:
                return f"Run or revise {command}; {', '.join(errors)} is not approval-ready."
            return "Complete and review docs/architecture/project-brief.md before approving brief."
        return f"Review and approve GATE=\"{gate}\"."
    delivery_status = state.get("delivery", {}).get("status", "not-started")
    if delivery_status == "draft":
        return "Core SAM is complete. Revise or approve the optional delivery handoff."
    if delivery_status == "approved":
        return "Core SAM and optional delivery handoff are approved."
    return "Core SAM is complete. Run @sam handoff only if implementation slices are needed."


def reopen(args: argparse.Namespace) -> None:
    if args.gate not in GATES:
        fail(f"Unknown gate: {args.gate}")
    state = load_state()
    if args.gate in CORE_GATE_ORDER:
        start = CORE_GATE_ORDER.index(args.gate)
        affected_gates = CORE_GATE_ORDER[start:]
        for index, gate in enumerate(affected_gates):
            status = "draft" if index == 0 else "superseded"
            for key in GATES[gate]:
                if ARTIFACTS[key].exists():
                    if key != "project-brief":
                        sync_markdown_status(ARTIFACTS[key], status.title())
                    state["artifacts"][key] = {"path": str(ARTIFACTS[key]), "status": status, "hash": content_hash(ARTIFACTS[key])}
        state["currentGate"] = args.gate
        for key in ["delivery-plan", "delivery-design-system"]:
            if ARTIFACTS[key].exists():
                sync_markdown_status(ARTIFACTS[key], "Superseded")
                state["artifacts"][key] = {"path": str(ARTIFACTS[key]), "status": "superseded", "hash": content_hash(ARTIFACTS[key])}
        if state.get("delivery", {}).get("status") != "not-started":
            state["delivery"]["status"] = "superseded"
    else:
        for key in GATES[args.gate]:
            if ARTIFACTS[key].exists():
                sync_markdown_status(ARTIFACTS[key], "Draft")
                state["artifacts"][key] = {"path": str(ARTIFACTS[key]), "status": "draft", "hash": content_hash(ARTIFACTS[key])}
        if args.gate == "delivery":
            state["delivery"]["status"] = "draft"
    state.setdefault("reopenings", []).append({"gate": args.gate, "reason": args.reason, "at": now_iso()})
    save_state(state)
    write_index(state)
    print(f"Reopened {args.gate}; dependent artifacts are no longer authoritative")


def status(_args: argparse.Namespace) -> None:
    state = load_state()
    write_index(state)
    print(f"Root: {DOC_ROOT}")
    print(f"Current core gate: {state.get('currentGate', 'brief')}")
    print(f"Optional delivery: {state.get('delivery', {}).get('status', 'not-started')}")
    print("Artifacts:")
    for key, path in ARTIFACTS.items():
        print(f"- {key}: {artifact_status(state, key)} ({path})")
    print(f"Next: {next_action(state)}")


def next_cmd(_args: argparse.Namespace) -> None:
    print(next_action(load_state()))


def handoff(_args: argparse.Namespace) -> None:
    state = load_state()
    init_delivery(state)
    print(f"Initialized optional delivery handoff at {DELIVERY_ROOT}")


def validate_cmd(args: argparse.Namespace) -> None:
    if args.artifact == "all":
        keys = [key for key, path in ARTIFACTS.items() if path.exists() and key in REQUIRED_SECTIONS]
    else:
        keys = [args.artifact]
    unknown = [key for key in keys if key not in ARTIFACTS]
    if unknown:
        fail("Unknown artifact(s): " + ", ".join(unknown))
    failures = {key: validate_artifact(key) for key in keys}
    failures = {key: errors for key, errors in failures.items() if errors}
    if failures:
        fail("; ".join(f"{key}: {', '.join(errors)}" for key, errors in failures.items()))
    print("Validation passed: " + ", ".join(keys))


def template_parity(args: argparse.Namespace) -> None:
    method_root = Path(args.method_root)
    mismatches = []
    for asset_name, method_path in TEMPLATE_PARITY.items():
        asset = TEMPLATE_ROOT / asset_name
        source = method_root / method_path
        if not asset.exists() or not source.exists():
            mismatches.append(f"missing pair: {asset} / {source}")
        elif asset.read_bytes() != source.read_bytes():
            mismatches.append(f"template differs: {asset_name} != {source}")
    if mismatches:
        fail("; ".join(mismatches))
    print("Template parity passed")


def validate_examples(args: argparse.Namespace) -> None:
    examples_root = Path(args.examples_root).resolve()
    domains = sorted(path for path in examples_root.iterdir() if path.is_dir())
    failures = []
    cwd = Path.cwd()
    for domain in domains:
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                DOC_ROOT.mkdir(parents=True)
                shutil.copy2(domain / "input" / "project-brief.md", ARTIFACTS["project-brief"])
                for directory in [
                    "01-architectural-requirements", "02-architectural-design",
                    "03-architectural-documentation", "delivery",
                ]:
                    source = domain / directory
                    if source.exists():
                        shutil.copytree(source, DOC_ROOT / directory)
                state = default_state(domain.name)
                for key, path in ARTIFACTS.items():
                    if path.exists():
                        state["artifacts"][key] = {"path": str(path), "status": "draft", "hash": content_hash(path)}
                save_state(state)
                for key in [
                    "phase-1-drivers", "phase-2-iteration-plan", "phase-2-decisions",
                    "phase-3-document", "delivery-plan",
                ]:
                    if ARTIFACTS[key].exists():
                        mark_draft(argparse.Namespace(artifact=key))
                keys = ["project-brief", "phase-1-drivers", "phase-2-iteration-plan", "phase-2-decisions", "phase-3-document"]
                if ARTIFACTS["delivery-plan"].exists():
                    keys.append("delivery-plan")
                domain_errors = {key: validate_artifact(key) for key in keys}
                domain_errors = {key: errors for key, errors in domain_errors.items() if errors}
                if domain_errors:
                    failures.append(f"{domain.name}: " + "; ".join(f"{key}: {', '.join(errors)}" for key, errors in domain_errors.items()))
            finally:
                os.chdir(cwd)
    if failures:
        fail("\n".join(failures))
    print("Example validation passed: " + ", ".join(domain.name for domain in domains))


def _expect_failure(action) -> None:
    try:
        action()
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("expected action to fail")


def _write_valid_brief() -> None:
    parts = ["# Demo - Project Brief"]
    for index, section in enumerate(REQUIRED_SECTIONS["project-brief"], 1):
        parts.append(f"## {index}. {section}\n\nMeaningful project information for {section.lower()} and architect review.")
    ARTIFACTS["project-brief"].write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def _metadata(title: str) -> str:
    return f"""# {title}

Status: Draft
Generated by: SAM agent
Approved by:
Approved date:
Rigor profile: Lite
System context: Greenfield
Source artifacts:
"""


def _write_valid_core_artifacts() -> None:
    ARTIFACTS["phase-1-drivers"].write_text(_metadata("Drivers") + """
## 1. Intake Summary
Meaningful approved intake summary.
## 2. ASR Classification
| ID | Requirement | Type | Source | Significance | Gap |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | Deliver useful behavior | Significant functionality | Brief | Shapes behavior | None |
## 3. Quality Attribute Scenarios
| ID | Attribute | Source | Stimulus | Artifact | Environment | Response | Measure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QA-001 | Performance | User | Requests page | System | Normal | Respond | Under 1 second |
## 4. Assumptions And Concerns
| ID | Assumption | Impact | Owner | Resolution |
| --- | --- | --- | --- | --- |
| CON-001 | Managed hosting | Deployment | Architect | Accepted |
## 5. Utility Tree
| Driver | Business | Difficulty | Risk | Priority |
| --- | --- | --- | --- | --- |
| Performance | High | Medium | Medium | Primary |
## 6. Driver Proposal
| Driver ID | Driver | Priority | Sources | Rationale | Tradeoff |
| --- | --- | --- | --- | --- | --- |
| DRV-001 | Fast response | Primary | REQ-001, QA-001 | User conversion | Cost |
## 7. Open Questions And Risks
| Item | Owner | Effect | Resolution |
| --- | --- | --- | --- |
| Hosting limit | Architect | Capacity | Accepted for MVP |
## 8. Exit Checklist
- [x] Complete intake.
- [x] Unique measurable drivers.
- [x] Risks owned.
- [x] Sources reviewed.
""", encoding="utf-8")
    mark_draft(argparse.Namespace(artifact="phase-1-drivers"))

    ARTIFACTS["phase-2-iteration-plan"].write_text(_metadata("Iterations") + """
## 1. Design Context
Approved drivers and constraints shape one iteration.
## 2. Iteration Plan
| Iteration | Goal | Element | Drivers | Output | Complete |
| --- | --- | --- | --- | --- | --- |
| 1 | Structure | System | DRV-001 | Decision | Reviewed |
## 3. Execution Record
| Iteration | Status | Result | Remaining | Review |
| --- | --- | --- | --- | --- |
| 1 | Reviewed | Complete | None | Accepted |
## 4. Exit Checklist
- [x] Drivers assigned.
- [x] Proportional design.
- [x] Sources reviewed.
""", encoding="utf-8")
    mark_draft(argparse.Namespace(artifact="phase-2-iteration-plan"))

    ARTIFACTS["phase-2-decisions"].write_text(_metadata("Decisions") + """
## 1. Selected Concepts And Tradeoffs
| Iteration | Drivers | Concept | Benefits | Costs | Alternatives |
| --- | --- | --- | --- | --- | --- |
| 1 | DRV-001 | Static delivery | Fast | Build step | Dynamic server |
## 2. Instantiated Elements And Interfaces
| Iteration | Element | Responsibility | Rationale | Change |
| --- | --- | --- | --- | --- |
| 1 | CDN | Deliver assets | Performance | New |
## 3. Architectural Decisions
| ID | Drivers | Decision | Rationale | Alternatives | Consequences | Triggers | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADR-001 | DRV-001 | Use CDN | Fast delivery | Server | Cache invalidation | Failed check | Draft |
## 4. Provisional Views
Audience: implementer. Question: delivery boundary. Elements: browser and CDN. Relations: HTTPS. Legend: arrow means request.
## 5. Driver Coverage And Evidence Plan
| Driver | Coverage | ADR | Check | Evidence | Next |
| --- | --- | --- | --- | --- | --- |
| DRV-001 | Addressed | ADR-001 | CHECK-001 | Performance result | Execute |
## 6. Risks And Follow-Up
| Risk | Drivers | Owner | Mitigation |
| --- | --- | --- | --- |
| Cache staleness | DRV-001 | Team | Version assets |
## 7. Exit Checklist
- [x] Design recorded.
- [x] Coverage complete.
- [x] ADR complete.
- [x] No false verification.
- [x] Sources reviewed.
""", encoding="utf-8")
    mark_draft(argparse.Namespace(artifact="phase-2-decisions"))

    ARTIFACTS["phase-3-document"].write_text(_metadata("Architecture") + """
## 1. Purpose, Audiences And Uses
Implementers use this document to preserve delivery constraints.
## 2. System Context And Scope
The system serves a public page through managed delivery.
## 3. Architectural Drivers And Scenarios
DRV-001 requires QA-001 response under one second.
## 4. View Selection
One delivery view answers the implementer boundary question.
## 5. Architecture Views
Audience: implementer. Question: delivery. Browser requests assets from CDN. Legend: arrow means HTTPS.
## 6. Architectural Decisions
ADR-001 uses CDN delivery with cache consequences.
## 7. Interfaces And Runtime Behavior
HTTPS asset requests are the only runtime interface.
## 8. Quality, Security, Data And Operations
TLS, cache metrics, deployment rollback, and accessibility checks apply.
## 9. Traceability And Evidence
| Requirement | Scenario | Driver | ADR | View | Check | Status |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | QA-001 | DRV-001 | ADR-001 | Delivery | CHECK-001 | Pending |
## 10. Risks, Assumptions And Technical Debt
Cache invalidation remains an owned operational risk.
## 11. Governance And Agent Guidance
Agents read approved decisions and reopen the gate before contradiction.
## 12. Exit Checklist
- [x] Audiences drive views.
- [x] Views agree.
- [x] Traceability complete.
- [x] Concerns addressed.
- [x] Sources and approvals current.
""", encoding="utf-8")


def self_test(_args: argparse.Namespace) -> None:
    cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            _expect_failure(lambda: can_run(argparse.Namespace(step="step-one")))
            init(argparse.Namespace(name="Demo"))
            assert AGENTS_START in AGENTS_PATH.read_text(encoding="utf-8")
            first_agents = AGENTS_PATH.read_text(encoding="utf-8")
            write_agents_block()
            assert AGENTS_PATH.read_text(encoding="utf-8") == first_agents
            assert "three-phase" not in INDEX_PATH.read_text(encoding="utf-8").lower() or INDEX_PATH.exists()
            _expect_failure(lambda: approve(argparse.Namespace(gate="brief", approved_by="Architect")))
            _write_valid_brief()
            approve(argparse.Namespace(gate="brief", approved_by="Architect"))
            assert "step-one" in next_action(load_state())

            _write_valid_core_artifacts()
            original = ARTIFACTS["phase-1-drivers"].read_text(encoding="utf-8")
            driver_row = "| DRV-001 | Fast response | Primary | REQ-001, QA-001 | User conversion | Cost |"
            duplicate = original.replace(driver_row, driver_row + "\n| DRV-001 | Duplicate | Primary | QA-001 | Duplicate | None |")
            ARTIFACTS["phase-1-drivers"].write_text(duplicate, encoding="utf-8")
            assert any("duplicate DRV" in error for error in validate_artifact("phase-1-drivers"))
            ARTIFACTS["phase-1-drivers"].write_text(original, encoding="utf-8")
            approve(argparse.Namespace(gate="phase-1-drivers", approved_by="Architect"))
            mark_draft(argparse.Namespace(artifact="phase-2-iteration-plan"))
            mark_draft(argparse.Namespace(artifact="phase-2-decisions"))
            approve(argparse.Namespace(gate="phase-2-design", approved_by="Architect"))
            mark_draft(argparse.Namespace(artifact="phase-3-document"))

            invalid = ARTIFACTS["phase-3-document"].read_text(encoding="utf-8").replace("| Pending |", "| Verified |")
            valid = ARTIFACTS["phase-3-document"].read_text(encoding="utf-8")
            ARTIFACTS["phase-3-document"].write_text(invalid, encoding="utf-8")
            assert any("Verified requires" in error for error in validate_artifact("phase-3-document"))
            ARTIFACTS["phase-3-document"].write_text(valid, encoding="utf-8")
            approve(argparse.Namespace(gate="phase-3-document", approved_by="Architect"))
            assert load_state()["currentGate"] == "complete"
            can_run(argparse.Namespace(step="step-four"))

            handoff(argparse.Namespace())
            ARTIFACTS["delivery-plan"].write_text(_metadata("Delivery") + """
## 1. Authoritative Sources
Approved architecture and decisions provide constraints.
## 2. Delivery And Technology Constraints
CDN delivery follows ADR-001 and DRV-001.
## 3. Implementation Order
SLICE-001 delivers the static page first.
## 4. Implementation Slices
### SLICE-001 - Static Delivery
Outcome, boundaries, tests, CHECK-001 evidence, risks, rollback, and done conditions are defined.
## 5. Code Agent Prompt
Implement only SLICE-001 after reading approved architecture.
## 6. Slice Governance And Evidence
| Driver | Slice | Check | Dependency | Rollback |
| --- | --- | --- | --- | --- |
| DRV-001 | SLICE-001 | CHECK-001 | None | Restore prior deployment |
## 7. Exit Checklist
- [x] Driver trace complete.
- [x] Boundaries and rollback explicit.
- [x] Criteria and checks separate.
- [x] Approved sources recorded.
""", encoding="utf-8")
            mark_draft(argparse.Namespace(artifact="delivery-plan"))
            approve(argparse.Namespace(gate="delivery", approved_by="Architect"))
            can_run(argparse.Namespace(step="slice"))

            ARTIFACTS["phase-1-drivers"].write_text(ARTIFACTS["phase-1-drivers"].read_text(encoding="utf-8") + "\nChanged.\n", encoding="utf-8")
            assert artifact_status(load_state(), "phase-1-drivers") == "drift"
            assert "drift" in next_action(load_state()).lower()
            reopen(argparse.Namespace(gate="phase-1-drivers", reason="driver changed"))
            assert artifact_status(load_state(), "phase-3-document") == "superseded"
            assert load_state()["delivery"]["status"] == "superseded"

            migration = Path("migration")
            migration.mkdir()
            os.chdir(migration)
            legacy = Path("docs/architecture/04-architectural-implementation")
            legacy.mkdir(parents=True)
            (legacy / "implementation-plan.md").write_text("legacy\n", encoding="utf-8")
            STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            STATE_PATH.write_text(json.dumps({
                "version": 2,
                "currentGate": "phase-4-implementation",
                "artifacts": {"phase-4-implementation-plan": {"status": "draft", "path": str(legacy / "implementation-plan.md")}},
                "approvals": [],
            }), encoding="utf-8")
            migrated = load_state()
            assert migrated["version"] == 3
            assert migrated["currentGate"] == "complete"
            assert DELIVERY_ROOT.exists()
        finally:
            os.chdir(cwd)
    print("sam_state self-test passed")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SAM three-phase state helper")
    sub = parser.add_subparsers(dest="command", required=True)

    init_p = sub.add_parser("init")
    init_p.add_argument("--name", default="Project")
    init_p.set_defaults(func=init)

    sub.add_parser("status").set_defaults(func=status)
    sub.add_parser("next").set_defaults(func=next_cmd)
    sub.add_parser("handoff").set_defaults(func=handoff)

    mark_p = sub.add_parser("mark-draft")
    mark_p.add_argument("artifact")
    mark_p.set_defaults(func=mark_draft)

    approve_p = sub.add_parser("approve")
    approve_p.add_argument("gate")
    approve_p.add_argument("--approved-by", default="Architect")
    approve_p.set_defaults(func=approve)

    reopen_p = sub.add_parser("reopen")
    reopen_p.add_argument("gate")
    reopen_p.add_argument("--reason", required=True)
    reopen_p.set_defaults(func=reopen)

    can_p = sub.add_parser("can-run")
    can_p.add_argument("step")
    can_p.set_defaults(func=can_run)

    validate_p = sub.add_parser("validate")
    validate_p.add_argument("artifact", nargs="?", default="all")
    validate_p.set_defaults(func=validate_cmd)

    parity_p = sub.add_parser("template-parity")
    parity_p.add_argument("--method-root", default="method")
    parity_p.set_defaults(func=template_parity)

    examples_p = sub.add_parser("validate-examples")
    examples_p.add_argument("--examples-root", default="examples")
    examples_p.set_defaults(func=validate_examples)

    sub.add_parser("self-test").set_defaults(func=self_test)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
