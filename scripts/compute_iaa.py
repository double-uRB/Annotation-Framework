"""Compute IAA metrics for classification and entity extraction.

Expected input is a JSON file with two top-level arrays, ``reference`` and
``candidate``. Each array contains records shaped like the D1 annotation schema.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from sklearn.metrics import cohen_kappa_score, confusion_matrix, f1_score, precision_recall_fscore_support


def load_json_or_jsonl(path: Path) -> Any:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def document_id(record: dict[str, Any]) -> str:
    return record["document_metadata"]["document_id"]


def align_records(reference: list[dict[str, Any]], candidate: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidate_by_id = {document_id(record): record for record in candidate}
    aligned_reference = []
    aligned_candidate = []
    missing = []
    for record in reference:
        doc_id = document_id(record)
        if doc_id not in candidate_by_id:
            missing.append(doc_id)
            continue
        aligned_reference.append(record)
        aligned_candidate.append(candidate_by_id[doc_id])
    if missing:
        raise ValueError(f"Candidate annotations missing {len(missing)} document(s): {', '.join(missing[:10])}")
    return aligned_reference, aligned_candidate


def safe_cohens_kappa(reference_labels: list[str], candidate_labels: list[str], labels: list[str] | None = None) -> float:
    if len(set(reference_labels) | set(candidate_labels)) <= 1:
        return 1.0 if reference_labels == candidate_labels else 0.0
    return float(cohen_kappa_score(reference_labels, candidate_labels, labels=labels))


def bbox_jaccard(a: list[float], b: list[float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)
    inter = max(0.0, inter_x2 - inter_x1) * max(0.0, inter_y2 - inter_y1)
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = area_a + area_b - inter
    return inter / union if union else 0.0


def is_strict_match(ref: dict[str, Any], cand: dict[str, Any]) -> bool:
    return ref["entity_type"] == cand["entity_type"] and ref["bounding_box"] == cand["bounding_box"]


def is_relaxed_match(ref: dict[str, Any], cand: dict[str, Any], threshold: float = 0.50) -> bool:
    return ref["entity_type"] == cand["entity_type"] and bbox_jaccard(ref["bounding_box"], cand["bounding_box"]) >= threshold


def match_entities(reference_entities: list[dict[str, Any]], candidate_entities: list[dict[str, Any]], relaxed: bool) -> tuple[int, int, int, list[float], int]:
    matcher = is_relaxed_match if relaxed else is_strict_match
    used_candidate_indexes = set()
    true_positive = 0
    overlaps = []
    boundary_matches = 0

    for ref in reference_entities:
        best_index = None
        best_overlap = -1.0
        for idx, cand in enumerate(candidate_entities):
            if idx in used_candidate_indexes or ref["entity_type"] != cand["entity_type"]:
                continue
            overlap = bbox_jaccard(ref["bounding_box"], cand["bounding_box"])
            if overlap > best_overlap:
                best_index = idx
                best_overlap = overlap
        if best_index is None:
            continue
        cand = candidate_entities[best_index]
        if matcher(ref, cand):
            true_positive += 1
            used_candidate_indexes.add(best_index)
            overlaps.append(best_overlap)
            if ref["bounding_box"][0] == cand["bounding_box"][0] and ref["bounding_box"][2] == cand["bounding_box"][2]:
                boundary_matches += 1

    false_positive = len(candidate_entities) - len(used_candidate_indexes)
    false_negative = len(reference_entities) - true_positive
    return true_positive, false_positive, false_negative, overlaps, boundary_matches


def prf(tp: int, fp: int, fn: int) -> dict[str, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def compute(reference: list[dict[str, Any]], candidate: list[dict[str, Any]]) -> dict[str, Any]:
    reference, candidate = align_records(reference, candidate)
    ref_labels = [record["classification"]["primary_type"] for record in reference]
    cand_labels = [record["classification"]["primary_type"] for record in candidate]
    labels = sorted(set(ref_labels) | set(cand_labels))

    class_kappa = safe_cohens_kappa(ref_labels, cand_labels, labels=labels)
    subtype_kappa = safe_cohens_kappa(
        [record["classification"]["subtype"] for record in reference],
        [record["classification"]["subtype"] for record in candidate],
    )

    per_type = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})
    strict_totals = {"tp": 0, "fp": 0, "fn": 0}
    relaxed_totals = {"tp": 0, "fp": 0, "fn": 0}
    relaxed_overlaps = []
    boundary_matches = 0
    relaxed_tp = 0

    for ref_doc, cand_doc in zip(reference, candidate):
        ref_entities = ref_doc.get("entities", [])
        cand_entities = cand_doc.get("entities", [])
        tp, fp, fn, _overlaps, _boundaries = match_entities(ref_entities, cand_entities, relaxed=False)
        strict_totals["tp"] += tp
        strict_totals["fp"] += fp
        strict_totals["fn"] += fn

        tp, fp, fn, overlaps, boundaries = match_entities(ref_entities, cand_entities, relaxed=True)
        relaxed_totals["tp"] += tp
        relaxed_totals["fp"] += fp
        relaxed_totals["fn"] += fn
        relaxed_overlaps.extend(overlaps)
        boundary_matches += boundaries
        relaxed_tp += tp

        for entity_type in sorted({e["entity_type"] for e in ref_entities} | {e["entity_type"] for e in cand_entities}):
            ref_subset = [e for e in ref_entities if e["entity_type"] == entity_type]
            cand_subset = [e for e in cand_entities if e["entity_type"] == entity_type]
            t, f_p, f_n, _o, _b = match_entities(ref_subset, cand_subset, relaxed=True)
            per_type[entity_type]["tp"] += t
            per_type[entity_type]["fp"] += f_p
            per_type[entity_type]["fn"] += f_n

    per_type_scores = {entity_type: prf(**counts) for entity_type, counts in sorted(per_type.items())}
    macro_f1 = sum(score["f1"] for score in per_type_scores.values()) / len(per_type_scores) if per_type_scores else 0.0
    exact_match_ratio = strict_totals["tp"] / (strict_totals["tp"] + strict_totals["fn"]) if strict_totals["tp"] + strict_totals["fn"] else 0.0

    return {
        "document_count": len(reference),
        "classification": {
            "primary_type_cohens_kappa": class_kappa,
            "subtype_cohens_kappa": subtype_kappa,
            "labels": labels,
            "confusion_matrix": confusion_matrix(ref_labels, cand_labels, labels=labels).tolist(),
        },
        "entity_extraction": {
            "strict": prf(**strict_totals),
            "relaxed": prf(**relaxed_totals),
            "macro_f1_by_entity_type": macro_f1,
            "per_entity_type": per_type_scores,
            "exact_match_ratio": exact_match_ratio,
            "mean_span_overlap_jaccard": sum(relaxed_overlaps) / len(relaxed_overlaps) if relaxed_overlaps else 0.0,
            "boundary_agreement": boundary_matches / relaxed_tp if relaxed_tp else 0.0,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute Cohen's Kappa and entity-level F1 for IAA.")
    parser.add_argument("--reference", type=Path, required=True, help="Gold/reference annotations JSON or JSONL.")
    parser.add_argument("--candidate", type=Path, required=True, help="Second annotator annotations JSON or JSONL.")
    parser.add_argument("--output", type=Path, help="Optional JSON output path.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    result = compute(load_json_or_jsonl(args.reference), load_json_or_jsonl(args.candidate))
    payload = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
