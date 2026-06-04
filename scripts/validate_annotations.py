"""Validate JSONL annotations against the project JSON Schema."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schema" / "annotation_schema.json"
DEFAULT_ANNOTATIONS = ROOT / "data" / "gold_standard" / "annotations.jsonl"


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        for line_number, line in enumerate(fh, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                yield line_number, json.loads(stripped)
            except json.JSONDecodeError as exc:
                yield line_number, exc


def validate(schema_path: Path, annotations_path: Path) -> int:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    checked = 0
    failures = 0

    for line_number, payload in iter_jsonl(annotations_path):
        checked += 1
        if isinstance(payload, json.JSONDecodeError):
            failures += 1
            print(f"[FAIL] line {line_number}: invalid JSON: {payload}", file=sys.stderr)
            continue

        errors = sorted(validator.iter_errors(payload), key=lambda err: list(err.path))
        if errors:
            failures += 1
            doc_id = payload.get("document_metadata", {}).get("document_id", f"line {line_number}")
            print(f"[FAIL] {doc_id}: {len(errors)} schema error(s)", file=sys.stderr)
            for error in errors[:10]:
                location = "/".join(str(part) for part in error.path) or "<root>"
                print(f"  - {location}: {error.message}", file=sys.stderr)
            if len(errors) > 10:
                print(f"  - ... {len(errors) - 10} more", file=sys.stderr)

    if checked == 0:
        print(f"[FAIL] no annotation records found in {annotations_path}", file=sys.stderr)
        return 1
    if failures:
        print(f"Validation failed: {failures}/{checked} records invalid.", file=sys.stderr)
        return 1

    print(f"Validation passed: {checked} records conform to {schema_path}.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate annotation JSONL against the FinSight schema.")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="Path to annotation_schema.json.")
    parser.add_argument("--annotations", type=Path, default=DEFAULT_ANNOTATIONS, help="Path to JSONL annotations.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(validate(args.schema, args.annotations))
