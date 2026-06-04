"""Generate the remaining 170 FinSight PDFs and JSONL annotations.

This script preserves the existing 30 Bank Statement annotations, generates the
other seven required categories, and rewrites the canonical annotations.jsonl
with all 200 records.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "data" / "raw_documents"
ANNOTATIONS_PATH = ROOT / "data" / "gold_standard" / "annotations.jsonl"
STATISTICS_PATH = ROOT / "data" / "gold_standard" / "statistics.json"

QUALITY_TAGS = [
    "CLEAN_DIGITAL",
    "OCR_HIGH_QUALITY",
    "OCR_DEGRADED",
    "OCR_NOISY",
    "MULTI_LANGUAGE",
    "MULTI_CURRENCY",
    "HANDWRITTEN_ELEMENTS",
    "REDACTED",
    "TEMPLATE_MISMATCH",
    "INCOMPLETE",
]

NON_EXACT_TAGS = [
    "CLEAN_DIGITAL",
    "OCR_HIGH_QUALITY",
    "HANDWRITTEN_ELEMENTS",
    "REDACTED",
    "TEMPLATE_MISMATCH",
    "INCOMPLETE",
]

TXN_TYPES = ["DEBIT", "CREDIT", "TRANSFER", "REVERSAL", "ADJUSTMENT", "REFUND"]


@dataclass(frozen=True)
class CategoryConfig:
    primary_type: str
    slug: str
    prefix: str
    count: int
    subtypes: list[str]
    issuers: list[str]
    products: list[str]


CATEGORIES = [
    CategoryConfig(
        "Commercial Invoice",
        "commercial_invoices",
        "INV",
        30,
        ["Tax Invoice", "Proforma Invoice", "Debit Note", "Credit Note", "Self-Invoice (Reverse Charge)"],
        ["Apex Components Pvt Ltd", "BluePeak Trading LLP", "Northstar Supplies Ltd"],
        ["Industrial Components", "Consulting Services", "Cloud Subscription"],
    ),
    CategoryConfig(
        "Income Tax Return",
        "income_tax_returns",
        "ITR",
        25,
        ["ITR-1 (Sahaj)", "ITR-2", "ITR-3", "ITR-4 (Sugam)", "ITR-5 (Firms)", "ITR-6 (Companies)", "ITR-7 (Trusts)"],
        ["Income Tax Department", "Central Board of Direct Taxes", "e-Filing Portal"],
        ["Income Tax Return", "Assessment Schedule", "Tax Computation"],
    ),
    CategoryConfig(
        "Loan Agreement",
        "loan_agreements",
        "LOAN",
        25,
        ["Personal Loan", "Home Loan / Mortgage", "Vehicle Loan", "Business Loan", "Overdraft Facility", "Line of Credit"],
        ["Horizon Finance Ltd", "Bharat Housing Finance", "Unity Cooperative Bank"],
        ["Floating Rate Loan", "Secured Term Loan", "Overdraft Facility"],
    ),
    CategoryConfig(
        "Insurance Policy",
        "insurance_policies",
        "POL",
        20,
        ["Term Life", "Health / Mediclaim", "Motor (Comprehensive/TP)", "Property / Fire", "Professional Indemnity", "Marine Cargo"],
        ["SecureLife Insurance Co", "Arogya Health Assurance", "National General Insurance"],
        ["Policy Schedule", "Coverage Rider", "Premium Notice"],
    ),
    CategoryConfig(
        "Regulatory Filing",
        "regulatory_filings",
        "REG",
        20,
        ["Annual Return (MCA)", "GST Return (GSTR-1/3B/9)", "TDS Return (26Q/27Q)", "SEBI Filing", "RBI Reporting"],
        ["Ministry of Corporate Affairs", "SEBI Compliance Portal", "Reserve Bank Reporting Desk"],
        ["Annual Return", "GST Filing", "Regulatory Disclosure"],
    ),
    CategoryConfig(
        "Payment Receipt",
        "payment_receipts",
        "RCPT",
        25,
        ["Cash Receipt", "Online Payment Confirmation", "Cheque Receipt", "Demand Draft Receipt", "UPI Payment Confirmation"],
        ["PaySwift Gateway", "Metro Retail Services", "Urban Utilities Ltd"],
        ["Payment Receipt", "UPI Confirmation", "Cash Collection Memo"],
    ),
    CategoryConfig(
        "Financial Statement",
        "financial_statements",
        "FS",
        25,
        ["Balance Sheet", "Profit & Loss Statement", "Cash Flow Statement", "Notes to Accounts", "Director Report Extract"],
        ["Orion Foods Ltd", "Prakash Textiles Pvt Ltd", "Veda Renewables Ltd"],
        ["Standalone Financial Statement", "Consolidated Statement", "Audited Notes"],
    ),
]

PARTIES = [
    ("Rajesh Kumar", "12 MG Road, Bengaluru, Karnataka 560001", "ABCDE1234F"),
    ("Priya Mehta", "88 Park Street, Kolkata, West Bengal 700016", "BCDEA2345G"),
    ("Aarav Exports Pvt Ltd", "Plot 42, MIDC Andheri, Mumbai, Maharashtra 400093", "27AABCA1234A1Z5"),
    ("Neha Sharma", "14 Civil Lines, Jaipur, Rajasthan 302006", "CDEAB3456H"),
    ("Zenith Traders LLP", "9 Ring Road, Surat, Gujarat 395002", "24AAAFZ6789L1Z2"),
]

LANGUAGE_NOTES = [
    "Spanish note: Pago recibido y verificado.",
    "French note: Montant a verifier avant cloture.",
    "Hindi note: Kripya rashi satyapit karein.",
]


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
        return {
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


class AnnotatedCanvas:
    def __init__(self, path: Path):
        self.path = path
        self.write_path = path.with_suffix(".tmp.pdf")
        self.canvas = Canvas(str(self.write_path), pagesize=A4)
        self.entities: list[Entity] = []
        self.entity_counter = 1
        self.page_number = 1

    def text(
        self,
        x: float,
        y: float,
        value: str,
        *,
        entity_type: str | None = None,
        normalized_value: Any = None,
        font: str = "Helvetica",
        size: int = 9,
        confidence: float = 0.99,
        notes: str = "",
    ) -> str | None:
        self.canvas.setFont(font, size)
        self.canvas.drawString(x, y, value)
        if not entity_type:
            return None
        width = self.canvas.stringWidth(value, font, size)
        entity_id = f"E{self.entity_counter:04d}"
        self.entity_counter += 1
        self.entities.append(
            Entity(
                entity_id,
                entity_type,
                value,
                normalized_value if normalized_value is not None else value,
                value,
                self.page_number,
                [x, y, x + width, y + size * 1.2],
                confidence,
                [],
                notes,
            )
        )
        return entity_id

    def box_entity(self, bbox: list[float], value: str, entity_type: str, normalized_value: Any) -> str:
        entity_id = f"E{self.entity_counter:04d}"
        self.entity_counter += 1
        self.entities.append(Entity(entity_id, entity_type, value, normalized_value, value, self.page_number, bbox))
        return entity_id

    def save(self) -> None:
        self.canvas.save()
        try:
            self.write_path.replace(self.path)
        except PermissionError:
            fallback = self.path.with_name(f"{self.path.stem}_{datetime.now().strftime('%H%M%S')}.pdf")
            self.write_path.replace(fallback)
            self.path = fallback


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def money(value: float, currency: str = "INR") -> str:
    return f"{currency} {value:,.2f}"


def money_norm(value: float, currency: str = "INR") -> dict[str, Any]:
    return {"amount": round(value, 2), "currency": currency}


def id_norm(value: str) -> dict[str, str]:
    return {"type": "GSTIN" if len(value) == 15 else "PAN", "value": value}


def quality_tags_for(global_index: int) -> list[str]:
    if 30 <= global_index <= 36:
        return ["MULTI_LANGUAGE"]
    if 37 <= global_index <= 48:
        return ["MULTI_CURRENCY"]
    if 49 <= global_index <= 58:
        return ["OCR_DEGRADED"]
    if 59 <= global_index <= 67:
        return ["OCR_NOISY"]
    return [NON_EXACT_TAGS[(global_index - 68) % len(NON_EXACT_TAGS)]]


def apply_visual_condition(ac: AnnotatedCanvas, tags: list[str], rng: random.Random) -> None:
    c = ac.canvas
    width, height = A4
    if "OCR_DEGRADED" in tags or "OCR_NOISY" in tags:
        c.setStrokeColor(colors.Color(0.65, 0.65, 0.65, alpha=0.35))
        line_count = 18 if "OCR_NOISY" in tags else 8
        for _ in range(line_count):
            y = rng.uniform(70, height - 90)
            c.line(rng.uniform(30, 80), y, rng.uniform(width - 140, width - 40), y + rng.uniform(-3, 3))
        c.setStrokeColor(colors.black)
    if "HANDWRITTEN_ELEMENTS" in tags:
        c.setFillColor(colors.HexColor("#273C75"))
        ac.text(370, 82, "Reviewed by A. Sen", entity_type="SIGNATURE_BLOCK", normalized_value={"name": "A. Sen", "designation": "Reviewer"}, font="Helvetica-Oblique", size=10)
        c.setFillColor(colors.black)
    if "REDACTED" in tags:
        c.setFillColor(colors.black)
        c.rect(420, 710, 80, 11, stroke=0, fill=1)
        c.setFillColor(colors.black)
    if "INCOMPLETE" in tags:
        c.setFillColor(colors.HexColor("#8A1C1C"))
        ac.text(50, 55, "Attachment pending: page 2 not supplied", font="Helvetica-Bold", size=8)
        c.setFillColor(colors.black)


def draw_header(
    ac: AnnotatedCanvas,
    config: CategoryConfig,
    doc_index: int,
    global_index: int,
    template_id: int,
    tags: list[str],
    rng: random.Random,
) -> dict[str, str | None]:
    c = ac.canvas
    width, height = A4
    palette = ["#244761", "#4C3B4D", "#395144", "#694E4E", "#385170", "#5C5470", "#3E606F", "#704214", "#2F4858", "#5B4B49"]
    color = colors.HexColor(palette[template_id % len(palette)])
    top = height - 42 - (template_id % 3) * 8
    c.setFillColor(color)
    c.rect(36, top - 34, width - 72, 34, stroke=0, fill=1)
    c.setFillColor(colors.white)

    doc_id = f"{config.prefix}-2024-{doc_index + 1:03d}"
    subtype = config.subtypes[doc_index % len(config.subtypes)]
    issuer = config.issuers[doc_index % len(config.issuers)]
    product = config.products[doc_index % len(config.products)]
    party, address, regulatory_id = PARTIES[(doc_index + template_id) % len(PARTIES)]
    issued = date(2024, 4, 1) + timedelta(days=(global_index * 3) % 240)
    fiscal = "FY2024-25"
    status = "Approved" if config.primary_type != "Insurance Policy" else "Active"

    institution_id = ac.text(50, top - 23, issuer, entity_type="INSTITUTION_NAME", font="Helvetica-Bold", size=13)
    document_id = ac.text(408, top - 22, doc_id, entity_type="DOCUMENT_ID", font="Helvetica-Bold", size=9)
    c.setFillColor(colors.black)
    ac.text(50, top - 58, subtype, font="Helvetica-Bold", size=12)
    product_id = ac.text(50, top - 76, product, entity_type="PRODUCT_NAME", font="Helvetica-Bold", size=9)
    party_id = ac.text(50, top - 96, party, entity_type="PARTY_NAME")
    ac.text(50, top - 113, address, entity_type="ADDRESS", size=8)
    ac.text(50, top - 131, regulatory_id, entity_type="REGULATORY_ID", normalized_value=id_norm(regulatory_id))
    date_text = "0l/03/2O24" if "OCR_NOISY" in tags else issued.strftime("%d-%b-%Y")
    ac.text(355, top - 76, date_text, entity_type="DATE", normalized_value=issued.isoformat(), confidence=0.72 if "OCR_NOISY" in tags else 0.99)
    ac.text(355, top - 96, fiscal, entity_type="FISCAL_PERIOD", normalized_value=fiscal)
    ac.text(355, top - 114, status, entity_type="STATUS", normalized_value=status)
    masked_account = f"****{rng.randint(1000, 9999)}"
    account_id = ac.text(355, top - 132, masked_account, entity_type="ACCOUNT_NUMBER", normalized_value=masked_account)
    currency_id = ac.text(510, top - 132, "INR", entity_type="CURRENCY_CODE", normalized_value="INR")
    ac.text(50, 72, "ops@finsight.example.com | +91-80-4000-1111", entity_type="CONTACT_INFO", normalized_value={"email": "ops@finsight.example.com", "phone": "+91-80-4000-1111"}, size=8)

    if "MULTI_LANGUAGE" in tags:
        ac.text(50, 92, LANGUAGE_NOTES[global_index % len(LANGUAGE_NOTES)], size=8, notes="Multi-language content injection.")

    return {
        "document_id": document_id,
        "institution_id": institution_id,
        "party_id": party_id,
        "account_id": account_id,
        "currency_id": currency_id,
        "product_id": product_id,
        "doc_id_value": doc_id,
        "subtype": subtype,
    }


def draw_table(ac: AnnotatedCanvas, x: float, y: float, headers: list[str], rows: list[list[str]], col_widths: list[int]) -> str:
    table_data = [headers] + rows
    table = Table(table_data, colWidths=col_widths, rowHeights=20)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5EDF4")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
                ("FONT", (0, 1), (-1, -1), "Helvetica", 8),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ]
        )
    )
    table.wrapOn(ac.canvas, A4[0], A4[1])
    table.drawOn(ac.canvas, x, y)
    return ac.box_entity([x, y, x + sum(col_widths), y + 20 * len(table_data)], "Structured table", "TABLE_DATA", {"columns": headers, "row_count": len(rows)})


def draw_amount_row(ac: AnnotatedCanvas, y: float, label: str, value: float, currency_id: str | None) -> str:
    ac.text(58, y, label, font="Helvetica-Bold", size=9)
    amount_id = ac.text(230, y, money(value), entity_type="MONETARY_AMOUNT", normalized_value=money_norm(value))
    if currency_id:
        ac.entities[-1].linked_entities.append(currency_id)
    return amount_id or ""


def draw_multi_currency(ac: AnnotatedCanvas, y: float) -> None:
    rows = [["USD", "1,250.00", "83.20", "INR 104,000.00"], ["EUR", "900.00", "89.50", "INR 80,550.00"]]
    table_id = draw_table(ac, 310, y, ["Currency", "Foreign Amt", "Rate", "INR Value"], rows, [55, 70, 55, 80])
    for row_index, row in enumerate(rows, start=1):
        row_bottom = y + (len(rows) - row_index) * 20
        code = row[0]
        ac.box_entity([314, row_bottom + 4, 360, row_bottom + 16], code, "CURRENCY_CODE", code)
        ac.box_entity([365, row_bottom + 4, 435, row_bottom + 16], row[1], "MONETARY_AMOUNT", money_norm(float(row[1].replace(",", "")), code))
    ac.text(310, y + 68, "FX conversion table", entity_type="COMPUTATION", normalized_value={"formula": "foreign_amount * fx_rate = INR value"}, size=8)


def draw_category_body(
    ac: AnnotatedCanvas,
    config: CategoryConfig,
    helpers: dict[str, str | None],
    doc_index: int,
    global_index: int,
    tags: list[str],
    rng: random.Random,
) -> None:
    currency_id = helpers["currency_id"]
    base = 15000 + doc_index * 821 + rng.randint(0, 1500)
    y = 560

    if config.primary_type == "Commercial Invoice":
        tax = round(base * 0.18, 2)
        total = base + tax
        draw_table(ac, 54, 355, ["Item", "Qty", "Rate", "GST", "Amount"], [["Service fee", "2", money(base / 2), "18%", money(base)], ["GST", "", "", "18%", money(tax)]], [150, 45, 90, 55, 100])
        draw_amount_row(ac, 525, "Subtotal", base, currency_id)
        draw_amount_row(ac, 505, "GST Amount", tax, currency_id)
        total_id = draw_amount_row(ac, 485, "Invoice Total", total, currency_id)
        ac.text(360, 505, "18%", entity_type="PERCENTAGE", normalized_value={"value": 18.0, "type": "GST"})
        ac.text(58, 462, "Total = subtotal + GST", entity_type="COMPUTATION", normalized_value={"formula": "total = subtotal + gst"})
        ac.text(58, 442, "CREDIT", entity_type="TRANSACTION_TYPE", normalized_value="CREDIT")
    elif config.primary_type == "Income Tax Return":
        income = base * 8
        tax_due = round(income * 0.12, 2)
        draw_table(ac, 54, 358, ["Schedule", "Reported", "Computed"], [["Gross Income", money(income), money(income)], ["Tax Due", money(tax_due), money(tax_due)]], [150, 130, 130])
        draw_amount_row(ac, 525, "Gross Total Income", income, currency_id)
        draw_amount_row(ac, 505, "Tax Payable", tax_due, currency_id)
        ac.text(58, 482, "12%", entity_type="PERCENTAGE", normalized_value={"value": 12.0, "type": "effective_tax_rate"})
        ac.text(58, 462, "Note 1", entity_type="FOOTNOTE_REF", normalized_value={"ref": "Note 1", "text": "Tax computed after rebate."})
        ac.text(58, 442, "Tax = income * effective rate", entity_type="COMPUTATION", normalized_value={"formula": "tax_payable = income * effective_tax_rate"})
    elif config.primary_type == "Loan Agreement":
        principal = base * 12
        draw_amount_row(ac, 525, "Sanctioned Amount", principal, currency_id)
        ac.text(58, 503, "9.25% p.a. floating", entity_type="INTEREST_RATE", normalized_value={"rate": 9.25, "period": "annual", "type": "floating"})
        ac.text(250, 503, "60 months", entity_type="DURATION", normalized_value={"value": 60, "unit": "months"})
        ac.text(58, 478, "Section 3.2(a)(ii)", entity_type="CLAUSE_REFERENCE", normalized_value="Section 3.2(a)(ii)")
        ac.text(58, 458, "Penalty per Section 8.1 applies on overdue EMI.", entity_type="CLAUSE_REFERENCE", normalized_value="Section 8.1")
        ac.text(58, 430, "Borrower Signature: Rajesh Kumar, 15-Apr-2024", entity_type="SIGNATURE_BLOCK", normalized_value={"name": "Rajesh Kumar", "designation": "Borrower", "date": "2024-04-15"})
    elif config.primary_type == "Insurance Policy":
        premium = base * 1.4
        cover = premium * 22
        draw_amount_row(ac, 525, "Annual Premium", premium, currency_id)
        draw_amount_row(ac, 505, "Sum Insured", cover, currency_id)
        ac.text(58, 482, "12 months", entity_type="DURATION", normalized_value={"value": 12, "unit": "months"})
        ac.text(180, 482, "5%", entity_type="PERCENTAGE", normalized_value={"value": 5.0, "type": "deductible"})
        ac.text(58, 460, "Exclusion Clause 4.3(b)", entity_type="CLAUSE_REFERENCE", normalized_value="Clause 4.3(b)")
        draw_table(ac, 54, 342, ["Coverage", "Limit", "Deductible"], [["Hospitalization", money(cover), "5%"], ["Rider", money(cover * 0.1), "0%"]], [150, 130, 90])
    elif config.primary_type == "Regulatory Filing":
        revenue = base * 20
        draw_amount_row(ac, 525, "Reported Turnover", revenue, currency_id)
        ac.text(58, 503, "INE123A01016", entity_type="REGULATORY_ID", normalized_value={"type": "ISIN", "value": "INE123A01016"})
        ac.text(58, 482, "Note 7", entity_type="FOOTNOTE_REF", normalized_value={"ref": "Note 7", "text": "Restated prior period figure."})
        ac.text(58, 462, "Schedule III, Part B", entity_type="CLAUSE_REFERENCE", normalized_value="Schedule III, Part B")
        draw_table(ac, 54, 342, ["Disclosure", "Current", "Prior"], [["Revenue", money(revenue), money(revenue * 0.9)], ["Liability", money(base * 4), money(base * 3.8)]], [150, 130, 130])
    elif config.primary_type == "Payment Receipt":
        paid = base * 0.8
        draw_amount_row(ac, 525, "Amount Paid", paid, currency_id)
        ac.text(58, 503, TXN_TYPES[doc_index % len(TXN_TYPES)], entity_type="TRANSACTION_TYPE", normalized_value=TXN_TYPES[doc_index % len(TXN_TYPES)])
        ac.text(180, 503, "UPI", entity_type="PRODUCT_NAME", normalized_value="UPI")
        ac.text(58, 482, "Approved", entity_type="STATUS", normalized_value="Approved")
        ac.text(58, 462, "Receipt amount reconciles to settlement batch", entity_type="COMPUTATION", normalized_value={"formula": "receipt_amount = settlement_batch_amount"})
    elif config.primary_type == "Financial Statement":
        assets = base * 30
        liabilities = base * 18
        equity = assets - liabilities
        draw_table(ac, 54, 342, ["Line Item", "Current Period", "Prior Period"], [["Assets", money(assets), money(assets * 0.93)], ["Liabilities", money(liabilities), money(liabilities * 0.91)], ["Equity", money(equity), money(equity * 0.96)]], [160, 130, 130])
        draw_amount_row(ac, 525, "Total Assets", assets, currency_id)
        draw_amount_row(ac, 505, "Total Liabilities", liabilities, currency_id)
        draw_amount_row(ac, 485, "Equity", equity, currency_id)
        ac.text(58, 462, "Assets = liabilities + equity", entity_type="COMPUTATION", normalized_value={"formula": "assets = liabilities + equity"})
        ac.text(58, 442, "Note 12", entity_type="FOOTNOTE_REF", normalized_value={"ref": "Note 12", "text": "Includes related party balances."})

    if "MULTI_CURRENCY" in tags:
        draw_multi_currency(ac, 250)


def make_relationships(entities: list[dict[str, Any]]) -> list[dict[str, str]]:
    by_type: dict[str, list[str]] = {}
    for entity in entities:
        by_type.setdefault(entity["entity_type"], []).append(entity["entity_id"])
    relationships: list[dict[str, str]] = []

    def add(kind: str, source: str | None, target: str | None) -> None:
        if source and target:
            relationships.append(
                {
                    "relationship_id": f"R{len(relationships) + 1:04d}",
                    "relationship_type": kind,
                    "source_entity_id": source,
                    "target_entity_id": target,
                }
            )

    add("ISSUED_BY", (by_type.get("DOCUMENT_ID") or [None])[0], (by_type.get("INSTITUTION_NAME") or [None])[0])
    add("HOLDER_OF_ACCOUNT", (by_type.get("PARTY_NAME") or [None])[0], (by_type.get("ACCOUNT_NUMBER") or [None])[0])
    add("DENOMINATED_IN", (by_type.get("MONETARY_AMOUNT") or [None])[0], (by_type.get("CURRENCY_CODE") or [None])[0])
    add("CONTAINS_TABLE", (by_type.get("DOCUMENT_ID") or [None])[0], (by_type.get("TABLE_DATA") or [None])[0])
    add("REFERENCES_CLAUSE", (by_type.get("MONETARY_AMOUNT") or [None])[0], (by_type.get("CLAUSE_REFERENCE") or [None])[0])
    add("FOOTNOTE_FOR", (by_type.get("FOOTNOTE_REF") or [None])[0], (by_type.get("MONETARY_AMOUNT") or [None])[0])
    add("SIGNED_BY", (by_type.get("SIGNATURE_BLOCK") or [None])[0], (by_type.get("PARTY_NAME") or [None])[0])
    add("EFFECTIVE_ON", (by_type.get("STATUS") or [None])[0], (by_type.get("DATE") or [None])[0])
    return relationships


PRIMARY_TYPE_MAP = {
    "Bank Statements": "Bank Statement",
    "Commercial Invoices": "Commercial Invoice",
    "Income Tax Returns": "Income Tax Return",
    "Loan Agreements": "Loan Agreement",
    "Insurance Policies": "Insurance Policy",
    "Regulatory Filings": "Regulatory Filing",
    "Payment Receipts": "Payment Receipt",
    "Financial Statements": "Financial Statement",
}

REVIEW_STATUS_MAP = {
    "pending_review": "Pending",
    "in_review": "Self-Reviewed",
    "approved": "Gold-Standard",
    "rejected": "Pending",
}


def normalize_record_for_active_schema(record: dict[str, Any]) -> dict[str, Any]:
    metadata = record["document_metadata"]
    metadata["review_status"] = REVIEW_STATUS_MAP.get(metadata.get("review_status"), metadata.get("review_status", "Pending"))

    classification = record["classification"]
    classification["primary_type"] = PRIMARY_TYPE_MAP.get(classification["primary_type"], classification["primary_type"])
    confidence_scores = classification.get("confidence_scores", {})
    classification["confidence_scores"] = {
        "primary_type": confidence_scores.get("primary_type", confidence_scores.get("primary_type_confidence", 0.99)),
        "subtype": confidence_scores.get("subtype", confidence_scores.get("subtype_confidence", 0.95)),
    }

    quality = record["quality_metadata"]
    if "ocr_confidence" not in quality:
        page_scores = quality.get("ocr_confidence_per_page", [{"confidence": 1.0}])
        quality["ocr_confidence"] = sum(page["confidence"] for page in page_scores) / len(page_scores)
    if "difficulty_rating" not in quality:
        quality["difficulty_rating"] = quality.get("annotation_difficulty", 3)
    if "time_to_annotate" not in quality:
        quality["time_to_annotate"] = quality.get("time_to_annotate_seconds", 0)
    record["quality_metadata"] = {
        "ocr_confidence": quality["ocr_confidence"],
        "difficulty_rating": quality["difficulty_rating"],
        "time_to_annotate": quality["time_to_annotate"],
        "review_comments": quality.get("review_comments", ""),
    }

    version = record["version_control"]
    record["version_control"] = {
        "schema_version": version.get("schema_version", "1.0.0"),
        "guideline_version": version.get("guideline_version", version.get("annotation_guideline_version", "1.0.0")),
        "annotator_tool_version": version.get("annotator_tool_version", "reportlab-generator"),
    }
    return record


def generate_document(config: CategoryConfig, doc_index: int, global_index: int, rng: random.Random) -> dict[str, Any]:
    template_count = math.ceil(config.count / 3)
    template_id = doc_index % template_count
    tags = quality_tags_for(global_index)
    out_dir = RAW_ROOT / config.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / f"{config.slug}_{doc_index + 1:03d}.pdf"
    ac = AnnotatedCanvas(pdf_path)
    helpers = draw_header(ac, config, doc_index, global_index, template_id, tags, rng)
    draw_category_body(ac, config, helpers, doc_index, global_index, tags, rng)
    apply_visual_condition(ac, tags, rng)
    ac.save()

    high_difficulty = any(tag in tags for tag in ["MULTI_LANGUAGE", "MULTI_CURRENCY", "OCR_DEGRADED", "OCR_NOISY", "INCOMPLETE", "TEMPLATE_MISMATCH"])
    timestamp = now_iso()
    entities = [entity.to_json() for entity in ac.entities]
    return {
        "document_metadata": {
            "document_id": str(helpers["doc_id_value"]),
            "source_file_path": str(ac.path.relative_to(ROOT)).replace("\\", "/"),
            "creation_date": timestamp,
            "last_modified": timestamp,
            "assigned_annotator": "synthetic_generator",
            "review_status": "Pending",
        },
        "classification": {
            "primary_type": config.primary_type,
            "subtype": str(helpers["subtype"]),
            "quality_tags": tags,
            "confidence_scores": {
                "primary_type": 0.99,
                "subtype": 0.95,
            },
        },
        "entities": entities,
        "relationships": make_relationships(entities),
        "quality_metadata": {
            "ocr_confidence": 0.74 if "OCR_NOISY" in tags else 0.86 if "OCR_DEGRADED" in tags else 0.98,
            "difficulty_rating": 4 if high_difficulty else 3,
            "time_to_annotate": rng.randint(480, 1260) if high_difficulty else rng.randint(300, 780),
            "review_comments": f"Visual template {template_id + 1}/{template_count}; generated by remaining corpus script.",
        },
        "version_control": {
            "schema_version": "1.0.0",
            "guideline_version": "1.0.0",
            "annotator_tool_version": "reportlab-remaining-corpus-1.0.0",
        },
    }


def load_existing_bank_records() -> list[dict[str, Any]]:
    if not ANNOTATIONS_PATH.exists():
        raise FileNotFoundError(f"Expected existing Bank Statement annotations at {ANNOTATIONS_PATH}")
    records = [json.loads(line) for line in ANNOTATIONS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    bank_records = [record for record in records if record["classification"]["primary_type"] in {"Bank Statements", "Bank Statement"}]
    if len(bank_records) != 30:
        raise ValueError(f"Expected 30 existing Bank Statement records, found {len(bank_records)}")
    return [normalize_record_for_active_schema(record) for record in bank_records]


def write_statistics(records: list[dict[str, Any]]) -> None:
    quality = Counter(tag for record in records for tag in record["classification"]["quality_tags"])
    categories = Counter(record["classification"]["primary_type"] for record in records)
    stats = {
        "document_count": len(records),
        "category_distribution": dict(sorted(categories.items())),
        "quality_tag_distribution": dict(sorted(quality.items())),
        "multi_language_documents": sum("MULTI_LANGUAGE" in record["classification"]["quality_tags"] for record in records),
        "multi_currency_documents": sum("MULTI_CURRENCY" in record["classification"]["quality_tags"] for record in records),
        "ocr_artifact_documents": sum(any(tag in record["classification"]["quality_tags"] for tag in ["OCR_DEGRADED", "OCR_NOISY"]) for record in records),
        "difficulty_4_or_5_documents": sum(record["quality_metadata"]["difficulty_rating"] >= 4 for record in records),
        "entity_type_distribution": dict(sorted(Counter(entity["entity_type"] for record in records for entity in record["entities"]).items())),
    }
    STATISTICS_PATH.write_text(json.dumps(stats, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def generate(seed: int) -> None:
    rng = random.Random(seed)
    records = load_existing_bank_records()
    global_index = len(records)
    for config in CATEGORIES:
        for doc_index in range(config.count):
            records.append(generate_document(config, doc_index, global_index, rng))
            global_index += 1
    ANNOTATIONS_PATH.write_text("".join(json.dumps(record, ensure_ascii=True) + "\n" for record in records), encoding="utf-8")
    write_statistics(records)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the remaining 170 PDFs and merge annotations.")
    parser.add_argument("--seed", type=int, default=20240605, help="Random seed for deterministic corpus generation.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generate(args.seed)
    print(f"Wrote merged annotations to {ANNOTATIONS_PATH}")
    print(f"Wrote statistics to {STATISTICS_PATH}")
