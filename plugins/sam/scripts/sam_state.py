#!/usr/bin/env python3
"""Small state helper for the SAM Codex plugin."""

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
STATE_PATH = DOC_ROOT / ".sam" / "state.json"

PHASE_DIRS = [
    DOC_ROOT / "01-architectural-requirements",
    DOC_ROOT / "02-architectural-design",
    DOC_ROOT / "03-architectural-documentation",
    DOC_ROOT / "04-architectural-implementation",
]

ARTIFACTS = {
    "project-brief": DOC_ROOT / "project-brief.md",
    "phase-1-input": DOC_ROOT / "01-architectural-requirements" / "input.md",
    "phase-1-drivers": DOC_ROOT / "01-architectural-requirements" / "architecture-drivers.md",
    "phase-2-input": DOC_ROOT / "02-architectural-design" / "input.md",
    "phase-2-iteration-plan": DOC_ROOT / "02-architectural-design" / "iteration-plan.md",
    "phase-2-decisions": DOC_ROOT / "02-architectural-design" / "design-decisions.md",
    "phase-3-input": DOC_ROOT / "03-architectural-documentation" / "input.md",
    "phase-3-document": DOC_ROOT / "03-architectural-documentation" / "architecture-document.md",
    "phase-4-input": DOC_ROOT / "04-architectural-implementation" / "input.md",
    "phase-4-implementation-plan": DOC_ROOT / "04-architectural-implementation" / "implementation-plan.md",
    "phase-4-design-system": DOC_ROOT / "04-architectural-implementation" / "design-system.md",
}

GATES = {
    "brief": ["project-brief"],
    "phase-1-drivers": ["phase-1-drivers"],
    "phase-2-design": ["phase-2-iteration-plan", "phase-2-decisions"],
    "phase-3-document": ["phase-3-document"],
    "phase-4-implementation": ["phase-4-implementation-plan"],
}

NEXT_GATE = {
    "brief": "phase-1-drivers",
    "phase-1-drivers": "phase-2-design",
    "phase-2-design": "phase-3-document",
    "phase-3-document": "phase-4-implementation",
    "phase-4-implementation": "complete",
}

REQUIRED_SECTIONS = {
    "project-brief": ["Business Problem", "System Goal", "Initial Scope / MVP", "Stakeholders", "Main Features", "Expected Quality Attributes", "Constraints", "Current Context", "Environments And Operations", "Customer Priorities"],
    "phase-1-drivers": ["Intake Summary", "ASR Classification", "Quality Attribute Scenarios", "Utility Tree", "Approved Driver Proposal", "Open Questions", "Exit Checklist"],
    "phase-2-iteration-plan": ["Context", "Iteration Plan", "Execution Summary", "Exit Checklist"],
    "phase-2-decisions": ["Selected Concepts", "Instantiation Decisions", "Architectural Decisions", "Provisional Design Views", "Driver Coverage And Pending Evidence", "Exit Checklist"],
    "phase-3-document": ["Introduction", "Context Diagram", "Architectural Drivers", "Architectural Decisions", "Scrum Handoff", "Traceability Matrix", "Governance Checks", "Exit Checklist"],
    "phase-4-implementation-plan": ["Source Artifacts", "Stack And Libraries", "Implementation Order", "Implementation Slices", "Exit Checklist"],
}

ID_REQUIREMENTS = {
    "phase-1-drivers": [r"\b(?:REQ|QA|CON)-\d{3}\b", r"\bDRV-\d{3}\b"],
    "phase-2-decisions": [r"\bDRV-\d{3}\b", r"\bADR-\d{3}\b", r"\bCHECK-\d{3}\b"],
    "phase-3-document": [r"\bDRV-\d{3}\b", r"\bADR-\d{3}\b", r"\bSTORY-\d{3}\b", r"\bCHECK-\d{3}\b"],
    "phase-4-implementation-plan": [r"\bSLICE-\d{3}\b", r"\bCHECK-\d{3}\b"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def fail(message: str, code: int = 2) -> None:
    print(message)
    raise SystemExit(code)


def migrate_legacy_workspace() -> None:
    """Move the misspelled v1 workspace only when the canonical path is absent."""
    if LEGACY_DOC_ROOT.exists() and not DOC_ROOT.exists():
        DOC_ROOT.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(LEGACY_DOC_ROOT), str(DOC_ROOT))
        print(f"Migrated legacy SAM workspace from {LEGACY_DOC_ROOT} to {DOC_ROOT}")
    elif LEGACY_DOC_ROOT.exists() and DOC_ROOT.exists():
        fail(
            f"Both {DOC_ROOT} and {LEGACY_DOC_ROOT} exist; merge them manually before continuing."
        )


def content_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def replace_metadata(text: str, field: str, value: str) -> str:
    pattern = rf"(?m)^{re.escape(field)}:.*$"
    replacement = f"{field}: {value}"
    if re.search(pattern, text):
        return re.sub(pattern, replacement, text, count=1)
    lines = text.splitlines()
    insert_at = 1 if lines else 0
    lines.insert(insert_at, replacement)
    return "\n".join(lines) + "\n"


def sync_markdown_status(path: Path, status_value: str, approved_by: str = "", approved_at: str = "") -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_metadata(text, "Status", status_value)
    if approved_by:
        text = replace_metadata(text, "Approved by", approved_by)
    if approved_at:
        text = replace_metadata(text, "Approved date", approved_at)
    path.write_text(text, encoding="utf-8")


def validate_artifact(key: str) -> list[str]:
    path = ARTIFACTS[key]
    if not path.exists():
        return ["artifact is missing"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if len(text.strip()) < 80:
        errors.append("artifact is empty or only a stub")
    for section in REQUIRED_SECTIONS.get(key, []):
        if not re.search(rf"(?m)^##+\s+(?:\d+\.\s+)?{re.escape(section)}\s*$", text):
            errors.append(f"missing section: {section}")
    for pattern in ID_REQUIREMENTS.get(key, []):
        if not re.search(pattern, text):
            errors.append(f"missing stable ID matching {pattern}")
    if key != "project-brief":
        for field in ["Status", "Generated by", "Approved by", "Approved date", "Source artifacts"]:
            if not re.search(rf"(?m)^{re.escape(field)}:", text):
                errors.append(f"missing metadata: {field}")
        if not re.search(r"(?m)^Tailoring profile: (?:Lite|Standard|High Assurance)$", text):
            errors.append("missing or invalid tailoring profile")
        if not re.search(r"(?m)^- .+ @ (?:version/hash:\s*)?\S+", text):
            errors.append("source artifact version/hash is missing")
        unchecked = re.findall(r"(?m)^- \[ \] (.+)$", text)
        if unchecked:
            errors.append("exit checklist contains unchecked items")
        if "Exit Checklist" in REQUIRED_SECTIONS.get(key, []) and not re.search(r"(?m)^- \[x\]", text):
            errors.append("exit checklist has no completed items")
    if "Satisfied for design" in text or "Partially satisfied" in text:
        errors.append("ambiguous design-validation status is not allowed")
    return errors


def default_state() -> dict:
    return {"version": 2, "currentGate": "brief", "artifacts": {}, "approvals": []}


def load_state() -> dict:
    migrate_legacy_workspace()
    if not STATE_PATH.exists():
        return default_state()
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def write_once(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def brief_template(name: str) -> str:
    title = name.strip() or "Project"
    return f"""# {title} - Project Brief

## 1. Business Problem

## 2. System Goal

## 3. Initial Scope / MVP

## 4. Stakeholders

## 5. Main Features

## 6. Expected Quality Attributes

## 7. Constraints

## 8. Current Context

## 9. Environments And Operations

## 10. Customer Priorities

## 11. Risk And Tailoring Inputs

## 12. Data, Security And Recovery
"""


def phase_input_template(phase: str) -> str:
    return f"""# {phase} Input

Status: Draft
Generated by: SAM agent
Approved by:
Approved date:
Tailoring profile: Lite / Standard / High Assurance
Source artifacts (path @ version/hash):

## Input

- 
"""


def init(args: argparse.Namespace) -> None:
    migrate_legacy_workspace()
    DOC_ROOT.mkdir(parents=True, exist_ok=True)
    for directory in PHASE_DIRS:
        directory.mkdir(parents=True, exist_ok=True)

    write_once(ARTIFACTS["project-brief"], brief_template(args.name))
    write_once(ARTIFACTS["phase-1-input"], phase_input_template("Phase 1 - Architectural Requirements"))
    write_once(ARTIFACTS["phase-2-input"], phase_input_template("Phase 2 - Architectural Design"))
    write_once(ARTIFACTS["phase-3-input"], phase_input_template("Phase 3 - Architectural Documentation"))
    write_once(ARTIFACTS["phase-4-input"], phase_input_template("Phase 4 - Architectural Implementation"))

    state = load_state()
    for key in ["project-brief", "phase-1-input", "phase-2-input", "phase-3-input", "phase-4-input"]:
        state["artifacts"].setdefault(key, {"path": str(ARTIFACTS[key]), "status": "draft"})
    save_state(state)
    print(f"Initialized SAM workspace at {DOC_ROOT}")


def artifact_status(state: dict, key: str) -> str:
    recorded = state.get("artifacts", {}).get(key, {}).get("status")
    if recorded:
        return recorded
    return "draft" if ARTIFACTS[key].exists() else "missing"


def mark_draft(args: argparse.Namespace) -> None:
    if args.artifact not in ARTIFACTS:
        fail(f"Unknown artifact: {args.artifact}")
    if not ARTIFACTS[args.artifact].exists():
        fail(f"Cannot mark missing artifact as draft: {ARTIFACTS[args.artifact]}")
    state = load_state()
    sync_markdown_status(ARTIFACTS[args.artifact], "Draft")
    state["artifacts"][args.artifact] = {
        "path": str(ARTIFACTS[args.artifact]), "status": "draft", "hash": content_hash(ARTIFACTS[args.artifact])
    }
    save_state(state)
    print(f"Marked draft: {args.artifact}")


def approve(args: argparse.Namespace) -> None:
    if args.gate not in GATES:
        fail(f"Unknown gate: {args.gate}")

    state = load_state()
    if state.get("currentGate", "brief") != args.gate:
        fail(f"Cannot approve {args.gate}; current gate is {state.get('currentGate', 'brief')}")
    missing = [key for key in GATES[args.gate] if not ARTIFACTS[key].exists()]
    if missing:
        fail("Cannot approve missing artifact(s): " + ", ".join(missing))

    validation_errors = {}
    for key in GATES[args.gate]:
        errors = validate_artifact(key)
        if errors:
            validation_errors[key] = errors
    if validation_errors:
        details = "; ".join(f"{key}: {', '.join(errors)}" for key, errors in validation_errors.items())
        fail(f"Cannot approve invalid artifact(s): {details}")

    approved_at = now_iso()
    source_versions = {
        key: content_hash(path) for key, path in ARTIFACTS.items() if path.exists()
    }
    for key in GATES[args.gate]:
        sync_markdown_status(ARTIFACTS[key], "Approved", args.approved_by, approved_at)
        state["artifacts"][key] = {
            "path": str(ARTIFACTS[key]), "status": "approved", "hash": content_hash(ARTIFACTS[key])
        }

    state["approvals"].append(
        {"gate": args.gate, "approvedBy": args.approved_by, "approvedAt": approved_at, "sourceVersions": source_versions}
    )
    state["currentGate"] = NEXT_GATE[args.gate]
    save_state(state)
    print(f"Approved {args.gate}; current gate is {state['currentGate']}")


def require_approved(state: dict, keys: list[str], step: str) -> None:
    missing = [key for key in keys if artifact_status(state, key) != "approved"]
    if missing:
        fail(f"{step} is blocked. Approval required for: {', '.join(missing)}")


def can_run(args: argparse.Namespace) -> None:
    state = load_state()
    step = args.step
    if step == "step-one":
        require_approved(state, ["project-brief"], step)
    elif step == "step-two":
        require_approved(state, ["phase-1-drivers"], step)
    elif step == "step-three":
        require_approved(state, ["phase-2-iteration-plan", "phase-2-decisions"], step)
    elif step == "step-four":
        require_approved(state, ["phase-3-document"], step)
    elif step == "slice":
        require_approved(state, ["phase-4-implementation-plan"], step)
    else:
        fail(f"Unknown step: {step}")
    print(f"OK: {step} is unblocked")


def next_action(state: dict) -> str:
    if not ARTIFACTS["project-brief"].exists():
        return "@sam init"
    gate = state.get("currentGate", "brief")
    if gate == "brief":
        return "Complete and approve docs/architecture/project-brief.md, then run @sam step-one."
    if gate == "phase-1-drivers":
        return "Approve phase-1-drivers or revise @sam step-one."
    if gate == "phase-2-design":
        return "Run @sam step-two after phase-1-drivers is approved."
    if gate == "phase-3-document":
        return "Run @sam step-three after phase-2-design is approved."
    if gate == "phase-4-implementation":
        return "Run @sam step-four after phase-3-document is approved."
    return "SAM workflow complete."


def validate_cmd(args: argparse.Namespace) -> None:
    keys = list(ARTIFACTS) if args.artifact == "all" else [args.artifact]
    unknown = [key for key in keys if key not in ARTIFACTS]
    if unknown:
        fail("Unknown artifact(s): " + ", ".join(unknown))
    failures = {key: validate_artifact(key) for key in keys}
    failures = {key: errors for key, errors in failures.items() if errors}
    if failures:
        fail("; ".join(f"{key}: {', '.join(errors)}" for key, errors in failures.items()))
    print("Validation passed: " + ", ".join(keys))


def reopen(args: argparse.Namespace) -> None:
    if args.gate not in GATES:
        fail(f"Unknown gate: {args.gate}")
    state = load_state()
    reached = False
    for gate, keys in GATES.items():
        if gate == args.gate:
            reached = True
        if reached:
            for key in keys:
                if ARTIFACTS[key].exists():
                    sync_markdown_status(ARTIFACTS[key], "Draft" if gate == args.gate else "Superseded")
                    state["artifacts"][key] = {
                        "path": str(ARTIFACTS[key]),
                        "status": "draft" if gate == args.gate else "superseded",
                        "hash": content_hash(ARTIFACTS[key]),
                    }
    state["currentGate"] = args.gate
    state.setdefault("reopenings", []).append({"gate": args.gate, "reason": args.reason, "at": now_iso()})
    save_state(state)
    print(f"Reopened {args.gate}; dependent artifacts marked Superseded")


def status(_args: argparse.Namespace) -> None:
    state = load_state()
    print(f"Root: {DOC_ROOT}")
    print(f"Current gate: {state.get('currentGate', 'brief')}")
    print("Artifacts:")
    for key, path in ARTIFACTS.items():
        print(f"- {key}: {artifact_status(state, key)} ({path})")
    print(f"Next: {next_action(state)}")


def next_cmd(_args: argparse.Namespace) -> None:
    print(next_action(load_state()))


def self_test(_args: argparse.Namespace) -> None:
    cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            try:
                can_run(argparse.Namespace(step="step-one"))
            except SystemExit as exc:
                assert exc.code == 2
            else:
                raise AssertionError("step-one should fail before init")

            init(argparse.Namespace(name="Demo"))
            assert ARTIFACTS["project-brief"].exists()
            try:
                can_run(argparse.Namespace(step="step-one"))
            except SystemExit:
                pass
            else:
                raise AssertionError("step-one should require brief approval")

            brief = ARTIFACTS["project-brief"].read_text(encoding="utf-8")
            brief = brief.replace("\n\n##", "\n\nComplete input.\n\n##") + "\nComplete input.\n"
            ARTIFACTS["project-brief"].write_text(brief, encoding="utf-8")
            approve(argparse.Namespace(gate="brief", approved_by="Architect"))
            can_run(argparse.Namespace(step="step-one"))

            def valid_artifact(key: str) -> None:
                sections = "\n\n".join(f"## {name}\n\nComplete content." for name in REQUIRED_SECTIONS[key])
                ids = "REQ-001 QA-001 CON-001 DRV-001 ADR-001 STORY-001 SLICE-001 CHECK-001"
                checklists = sections.replace("Complete content.", "Complete content.\n\n- [x] Validated")
                ARTIFACTS[key].parent.mkdir(parents=True, exist_ok=True)
                ARTIFACTS[key].write_text(
                    f"# Test\n\nStatus: Draft\nGenerated by: SAM agent\nApproved by:\nApproved date:\nTailoring profile: Lite\nSource artifacts:\n- source @ abc123\n\n{ids}\n\n{checklists}\n",
                    encoding="utf-8",
                )
                mark_draft(argparse.Namespace(artifact=key))

            ARTIFACTS["phase-1-drivers"].write_text("# Drivers\n", encoding="utf-8")
            try:
                approve(argparse.Namespace(gate="phase-1-drivers", approved_by="Architect"))
            except SystemExit:
                pass
            else:
                raise AssertionError("incomplete artifact should not be approved")
            valid_artifact("phase-1-drivers")
            approve(argparse.Namespace(gate="phase-1-drivers", approved_by="Architect"))
            can_run(argparse.Namespace(step="step-two"))

            try:
                approve(argparse.Namespace(gate="phase-3-document", approved_by="Architect"))
            except SystemExit:
                pass
            else:
                raise AssertionError("out-of-order approval should fail")

            valid_artifact("phase-2-iteration-plan")
            valid_artifact("phase-2-decisions")
            approve(argparse.Namespace(gate="phase-2-design", approved_by="Architect"))
            valid_artifact("phase-3-document")
            approve(argparse.Namespace(gate="phase-3-document", approved_by="Architect"))
            valid_artifact("phase-4-implementation-plan")
            approve(argparse.Namespace(gate="phase-4-implementation", approved_by="Architect"))
            can_run(argparse.Namespace(step="slice"))

            reopen(argparse.Namespace(gate="phase-2-design", reason="driver changed"))
            assert artifact_status(load_state(), "phase-3-document") == "superseded"

            state = load_state()
            assert state["currentGate"] == "phase-2-design"
            assert artifact_status(state, "phase-3-document") == "superseded"
        finally:
            os.chdir(cwd)
    print("sam_state self-test passed")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SAM state helper")
    sub = parser.add_subparsers(dest="command", required=True)

    init_p = sub.add_parser("init")
    init_p.add_argument("--name", default="Project")
    init_p.set_defaults(func=init)

    sub.add_parser("status").set_defaults(func=status)
    sub.add_parser("next").set_defaults(func=next_cmd)

    mark_p = sub.add_parser("mark-draft")
    mark_p.add_argument("artifact")
    mark_p.set_defaults(func=mark_draft)

    approve_p = sub.add_parser("approve")
    approve_p.add_argument("gate")
    approve_p.add_argument("--approved-by", default="Architect")
    approve_p.set_defaults(func=approve)

    validate_p = sub.add_parser("validate")
    validate_p.add_argument("artifact", nargs="?", default="all")
    validate_p.set_defaults(func=validate_cmd)

    reopen_p = sub.add_parser("reopen")
    reopen_p.add_argument("gate")
    reopen_p.add_argument("--reason", required=True)
    reopen_p.set_defaults(func=reopen)

    can_p = sub.add_parser("can-run")
    can_p.add_argument("step")
    can_p.set_defaults(func=can_run)

    sub.add_parser("self-test").set_defaults(func=self_test)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
