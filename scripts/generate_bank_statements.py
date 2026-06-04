"""Generate 30 synthetic Bank Statement PDFs and matching annotations.

The script records bounding boxes while drawing text with ReportLab, then emits
schema-conformant JSONL records for the generated PDFs.
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw_documents" / "bank_statements"
ANNOTATIONS_PATH = ROOT / "data" / "gold_standard" / "annotations.jsonl"

ENTITY_TYPES = {
    "MONETARY_AMOUNT",
    "DATE",
    "ACCOUNT_NUMBER",
    "PARTY_NAME",
    "REGULATORY_ID",
    "ADDRESS",
    "DOCUMENT_ID",
    "TRANSACTION_TYPE",
    "INSTITUTION_NAME",
    "PRODUCT_NAME",
    "STATUS",
    "CONTACT_INFO",
    "TABLE_DATA",
    "COMPUTATION",
    "CURRENCY_CODE",
    "FISCAL_PERIOD",
}

SUBTYPES = [
    "Savings Account Statement",
    "Current Account Statement",
    "Credit Card Statement",
    "Fixed Deposit Statement",
    "Demat Account Statement",
]

QUALITY_TAG_CYCLE = [
    ["CLEAN_DIGITAL"],
    ["OCR_HIGH_QUALITY"],
    ["OCR_DEGRADED"],
    ["OCR_NOISY"],
    ["MULTI_CURRENCY"],
    ["MULTI_LANGUAGE"],
    ["HANDWRITTEN_ELEMENTS"],
    ["REDACTED"],
    ["TEMPLATE_MISMATCH"],
    ["INCOMPLETE"],
]

BANKS = [
    "HDFC Bank Ltd",
    "ICICI Bank Ltd",
    "State Bank of India",
    "Axis Bank Ltd",
    "Kotak Mahindra Bank",
]

CUSTOMERS = [
    ("Rajesh Kumar", "12 MG Road, Bengaluru, Karnataka 560001", "ABCDE1234F"),
    ("Priya Mehta", "88 Park Street, Kolkata, West Bengal 700016", "BCDEA2345G"),
    ("Aarav Exports Pvt Ltd", "Plot 42, MIDC Andheri, Mumbai, Maharashtra 400093", "27AABCA1234A1Z5"),
    ("Neha Sharma", "14 Civil Lines, Jaipur, Rajasthan 302006", "CDEAB3456H"),
    ("Zenith Traders LLP", "9 Ring Road, Surat, Gujarat 395002", "24AAAFZ6789L1Z2"),
]

TXN_TYPES = ["DEBIT", "CREDIT", "TRANSFER", "REVERSAL", "ADJUSTMENT", "REFUND"]


@dataclass
class Entity:
    entity_id: str
    entity_type: str
    value: str
    normalized_value: Any
    source_text: str
    page_number: int
    bounding_box: list[float]
    confidence: float = 0.99
    linked_entities: list[str] | None = None
    annotator_notes: str = ""

    def __post_init__(self) -> None:
        if self.linked_entities is None:
            self.linked_entities = []

    def to_json(self) -> dict[str, Any]:
        data = {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "value": self.value,
            "normalized_value": self.normalized_value,
            "source_text": self.source_text,
            "page_number": self.page_number,
            "bounding_box": [round(v, 2) for v in self.bounding_box],
            "confidence": self.confidence,
            "linked_entities": self.linked_entities,
            "annotator_notes": self.annotator_notes,
        }
        return data


class AnnotatedCanvas:
    def __init__(self, path: Path):
        self.canvas = Canvas(str(path), pagesize=A4)
        self.entities: list[Entity] = []
        self.page_number = 1
        self.entity_counter = 1

    def text(
        self,
        x: float,
        y: float,
        value: str,
        *,
        font: str = "Helvetica",
        size: int = 9,
        entity_type: str | None = None,
        normalized_value: Any = None,
        confidence: float = 0.99,
        notes: str = "",
    ) -> str | None:
        self.canvas.setFont(font, size)
        self.canvas.drawString(x, y, value)
        if not entity_type:
            return None
        width = self.canvas.stringWidth(value, font, size)
        height = size * 1.2
        entity_id = f"E{self.entity_counter:04d}"
        self.entity_counter += 1
        self.entities.append(
            Entity(
                entity_id=entity_id,
                entity_type=entity_type,
                value=value,
                normalized_value=normalized_value if normalized_value is not None else value,
                source_text=value,
                page_number=self.page_number,
                bounding_box=[x, y, x + width, y + height],
                confidence=confidence,
                annotator_notes=notes,
            )
        )
        return entity_id

    def entity_box(
        self,
        bbox: list[float],
        value: str,
        *,
        entity_type: str,
        normalized_value: Any = None,
        confidence: float = 0.99,
        notes: str = "",
    ) -> str:
        entity_id = f"E{self.entity_counter:04d}"
        self.entity_counter += 1
        self.entities.append(
            Entity(
                entity_id=entity_id,
                entity_type=entity_type,
                value=value,
                normalized_value=normalized_value if normalized_value is not None else value,
                source_text=value,
                page_number=self.page_number,
                bounding_box=bbox,
                confidence=confidence,
                annotator_notes=notes,
            )
        )
        return entity_id

    def line(self, x1: float, y1: float, x2: float, y2: float) -> None:
        self.canvas.line(x1, y1, x2, y2)

    def page_break(self) -> None:
        self.canvas.showPage()
        self.page_number += 1

    def save(self) -> None:
        self.canvas.save()


def amount_text(value: float, currency: str = "INR") -> str:
    return f"{currency} {value:,.2f}"


def amount_norm(value: float, currency: str = "INR") -> dict[str, Any]:
    return {"amount": round(value, 2), "currency": currency}


def random_date(rng: random.Random, start: date, span_days: int) -> date:
    return start + timedelta(days=rng.randint(0, span_days))


def draw_statement(doc_index: int, out_dir: Path, rng: random.Random) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    subtype = SUBTYPES[doc_index % len(SUBTYPES)]
    bank = BANKS[doc_index % len(BANKS)]
    customer_name, address, regulatory_id = CUSTOMERS[doc_index % len(CUSTOMERS)]
    account_number = f"{rng.randint(10**11, 10**12 - 1)}"
    masked_account = f"****{account_number[-4:]}"
    statement_id = f"BS-2024-{doc_index + 1:03d}"
    start_date = date(2024, 4, 1) + timedelta(days=(doc_index % 6) * 30)
    end_date = start_date + timedelta(days=29)
    fiscal_period = "FY2024-25"
    status = "Approved"
    currency = "INR"
    quality_tags = QUALITY_TAG_CYCLE[doc_index % len(QUALITY_TAG_CYCLE)]
    if doc_index in {4, 14, 24} and "MULTI_CURRENCY" not in quality_tags:
        quality_tags = quality_tags + ["MULTI_CURRENCY"]

    pdf_path = out_dir / f"bank_statement_{doc_index + 1:03d}.pdf"
    ac = AnnotatedCanvas(pdf_path)
    c = ac.canvas
    width, height = A4

    c.setStrokeColor(colors.HexColor("#1F4E79"))
    c.setFillColor(colors.HexColor("#1F4E79"))
    c.rect(36, height - 72, width - 72, 36, stroke=0, fill=1)
    c.setFillColor(colors.white)
    ac.text(50, height - 58, bank, font="Helvetica-Bold", size=14, entity_type="INSTITUTION_NAME")
    ac.text(400, height - 58, statement_id, font="Helvetica-Bold", size=10, entity_type="DOCUMENT_ID")
    c.setFillColor(colors.black)

    ac.text(50, height - 95, subtype, font="Helvetica-Bold", size=12, entity_type="PRODUCT_NAME")
    ac.text(50, height - 118, customer_name, entity_type="PARTY_NAME")
    ac.text(50, height - 136, address, size=8, entity_type="ADDRESS")
    ac.text(50, height - 154, regulatory_id, entity_type="REGULATORY_ID", normalized_value={"type": "GSTIN" if len(regulatory_id) == 15 else "PAN", "value": regulatory_id})

    ac.text(350, height - 118, masked_account, entity_type="ACCOUNT_NUMBER", normalized_value=masked_account)
    ac.text(350, height - 136, start_date.strftime("%d-%b-%Y"), entity_type="DATE", normalized_value=start_date.isoformat())
    ac.text(442, height - 136, end_date.strftime("%d-%b-%Y"), entity_type="DATE", normalized_value=end_date.isoformat())
    ac.text(350, height - 154, fiscal_period, entity_type="FISCAL_PERIOD", normalized_value=fiscal_period)
    ac.text(470, height - 154, status, entity_type="STATUS", normalized_value=status)
    currency_id = ac.text(520, height - 154, currency, entity_type="CURRENCY_CODE", normalized_value=currency)

    opening = rng.randint(20_000, 180_000) + rng.random()
    transactions = []
    balance = opening
    for txn_index in range(10):
        txn_date = random_date(rng, start_date, 29)
        txn_type = rng.choice(TXN_TYPES)
        amt = round(rng.uniform(750, 55_000), 2)
        if txn_type in {"DEBIT", "TRANSFER", "ADJUSTMENT"}:
            balance -= amt
        else:
            balance += amt
        desc = rng.choice(["UPI transfer", "Salary credit", "Card settlement", "ATM withdrawal", "Interest credit", "NEFT payment"])
        transactions.append((txn_date, desc, txn_type, amt, balance))

    y = height - 200
    table_bbox = [44, y - (len(transactions) + 1) * 20, width - 44, y + 18]
    ac.entities.append(
        Entity(
            entity_id=f"E{ac.entity_counter:04d}",
            entity_type="TABLE_DATA",
            value="Transaction table",
            normalized_value={"columns": ["Date", "Description", "Type", "Amount", "Balance"], "row_count": len(transactions)},
            source_text="Transaction table",
            page_number=ac.page_number,
            bounding_box=table_bbox,
            confidence=0.98,
        )
    )
    table_entity_id = f"E{ac.entity_counter:04d}"
    ac.entity_counter += 1

    table_data = [["Date", "Description", "Type", "Amount", "Balance"]]
    for txn_date, desc, txn_type, amt, bal in transactions:
        table_data.append([txn_date.strftime("%d/%m/%Y"), desc, txn_type, amount_text(amt), amount_text(bal)])
    styles = getSampleStyleSheet()
    table = Table(table_data, colWidths=[70, 170, 75, 95, 95], rowHeights=20)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
                ("FONT", (0, 1), (-1, -1), "Helvetica", 8),
                ("ALIGN", (3, 1), (-1, -1), "RIGHT"),
            ]
        )
    )
    table.wrapOn(c, width, height)
    table.drawOn(c, 44, y - (len(transactions) + 1) * 20)

    table_x = 44
    table_bottom = y - (len(transactions) + 1) * 20
    col_x = [table_x, table_x + 70, table_x + 240, table_x + 315, table_x + 410, table_x + 505]
    first_row_top = table_bottom + len(transactions) * 20
    for row_index, (txn_date, _desc, txn_type, amt, bal) in enumerate(transactions, start=1):
        row_bottom = first_row_top - row_index * 20
        row_top = row_bottom + 20
        ac.entity_box([col_x[0] + 4, row_bottom + 4, col_x[1] - 4, row_top - 4], txn_date.strftime("%d/%m/%Y"), entity_type="DATE", normalized_value=txn_date.isoformat())
        txn_id = ac.entity_box([col_x[2] + 4, row_bottom + 4, col_x[3] - 4, row_top - 4], txn_type, entity_type="TRANSACTION_TYPE", normalized_value=txn_type)
        amount_id = ac.entity_box([col_x[3] + 4, row_bottom + 4, col_x[4] - 4, row_top - 4], amount_text(amt), entity_type="MONETARY_AMOUNT", normalized_value=amount_norm(amt, currency))
        ac.entity_box([col_x[4] + 4, row_bottom + 4, col_x[5] - 4, row_top - 4], amount_text(bal), entity_type="MONETARY_AMOUNT", normalized_value=amount_norm(bal, currency))
        if amount_id and currency_id:
            ac.entities[-2].linked_entities.append(currency_id)

    closing = balance
    summary_y = 120
    ac.text(50, summary_y, "Opening Balance", font="Helvetica-Bold", size=9)
    opening_id = ac.text(160, summary_y, amount_text(opening), entity_type="MONETARY_AMOUNT", normalized_value=amount_norm(opening, currency))
    ac.text(300, summary_y, "Closing Balance", font="Helvetica-Bold", size=9)
    closing_id = ac.text(410, summary_y, amount_text(closing), entity_type="MONETARY_AMOUNT", normalized_value=amount_norm(closing, currency))
    ac.text(50, summary_y - 24, "Closing balance = opening balance + credits - debits", entity_type="COMPUTATION", normalized_value={"formula": "closing_balance = opening_balance + credits - debits"})
    ac.text(50, 72, "care@bank.example.com | +91-80-4000-0000", size=8, entity_type="CONTACT_INFO", normalized_value={"email": "care@bank.example.com", "phone": "+91-80-4000-0000"})

    ac.save()

    entity_rows = [entity.to_json() for entity in ac.entities if entity.entity_type in ENTITY_TYPES]
    entity_ids_by_type = {}
    for entity in entity_rows:
        entity_ids_by_type.setdefault(entity["entity_type"], []).append(entity["entity_id"])

    relationships = []
    def add_rel(rel_type: str, source: str | None, target: str | None) -> None:
        if source and target:
            relationships.append(
                {
                    "relationship_id": f"R{len(relationships) + 1:04d}",
                    "relationship_type": rel_type,
                    "source_entity_id": source,
                    "target_entity_id": target,
                }
            )

    add_rel("HOLDER_OF_ACCOUNT", entity_ids_by_type.get("PARTY_NAME", [None])[0], entity_ids_by_type.get("ACCOUNT_NUMBER", [None])[0])
    add_rel("ISSUED_BY", entity_ids_by_type.get("DOCUMENT_ID", [None])[0], entity_ids_by_type.get("INSTITUTION_NAME", [None])[0])
    add_rel("DENOMINATED_IN", opening_id, currency_id)
    add_rel("DENOMINATED_IN", closing_id, currency_id)
    add_rel("CONTAINS_TABLE", entity_ids_by_type.get("DOCUMENT_ID", [None])[0], table_entity_id)

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "document_metadata": {
            "document_id": statement_id,
            "source_file_path": str(pdf_path.relative_to(ROOT)).replace("\\", "/"),
            "creation_date": now,
            "last_modified": now,
            "assigned_annotator": "synthetic_generator",
            "review_status": "pending_review",
        },
        "classification": {
            "primary_type": "Bank Statements",
            "subtype": subtype,
            "quality_tags": quality_tags,
            "confidence_scores": {
                "primary_type_confidence": 0.99,
                "subtype_confidence": 0.96,
            },
        },
        "entities": entity_rows,
        "relationships": relationships,
        "quality_metadata": {
            "ocr_confidence_per_page": [{"page": 1, "confidence": 0.78 if "OCR_NOISY" in quality_tags else 0.97}],
            "annotation_difficulty": 4 if any(tag in quality_tags for tag in ["OCR_NOISY", "MULTI_CURRENCY", "INCOMPLETE"]) else 3,
            "time_to_annotate_seconds": rng.randint(420, 900),
            "review_comments": "Synthetic bank statement generated with ReportLab and deterministic bounding boxes.",
        },
        "version_control": {
            "schema_version": "1.0.0",
            "annotation_guideline_version": "1.0.0",
            "annotator_tool_version": "reportlab-generator-1.0.0",
        },
    }


def generate(count: int, seed: int, output: Path) -> None:
    rng = random.Random(seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as fh:
        for index in range(count):
            annotation = draw_statement(index, RAW_DIR, rng)
            fh.write(json.dumps(annotation, ensure_ascii=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic bank statement PDFs and JSONL annotations.")
    parser.add_argument("--count", type=int, default=30, help="Number of Bank Statement PDFs to generate.")
    parser.add_argument("--seed", type=int, default=20240604, help="Random seed for reproducible output.")
    parser.add_argument("--output", type=Path, default=ANNOTATIONS_PATH, help="Output JSONL path.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generate(args.count, args.seed, args.output)
    print(f"Generated {args.count} PDFs in {RAW_DIR}")
    print(f"Wrote annotations to {args.output}")
