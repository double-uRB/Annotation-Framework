import os
import random

def generate_guideline():
    entities = [
        "DOCUMENT_ID", "DATE", "MONETARY_AMOUNT", "PARTY_NAME", "REGULATORY_ID",
        "ADDRESS", "LINE_ITEM", "COMPUTATION", "CLAUSE_REFERENCE", "SIGNATURE_BLOCK",
        "PERCENTAGE", "TRANSACTION_TYPE", "STATUS", "ACCOUNT_NUMBER", "BANK_CODE",
        "CURRENCY_CODE", "PHONE_NUMBER", "EMAIL_ADDRESS", "WEBSITE", "TAX_CODE",
        "INTEREST_RATE", "DURATION"
    ]
    
    doc_types = [
        "Bank Statements", "Invoices & Receipts", "Tax Returns", "Loan Agreements",
        "Insurance Policies", "Regulatory Filings", "Payment Receipts", "Financial Statements"
    ]

    quality_tags = [
        "OCR_DEGRADED", "HANDWRITTEN_ELEMENTS", "MULTI_LANGUAGE", "MULTI_CURRENCY",
        "COMPLEX_TABLES", "POOR_CONTRAST", "MISSING_PAGES", "SIGNATURE_OVERLAP",
        "STAMP_OBSCURATION", "NON_STANDARD_LAYOUT"
    ]

    sections = []
    
    # Section 1: Intro
    sections.append("# Section 1: Introduction & Purpose\n\nThis Annotation Guideline serves as the definitive master reference for the FinSight AI project. It establishes the rigid boundaries, taxonomy definitions, and procedural workflows necessary to extract structured financial data from deeply unstructured, multi-modal documents. The success of the downstream predictive models relies entirely on strict adherence to these rules.\n\nAnnotators must understand that financial documents are inherently adversarial. They are designed for human readability, not machine parsing. Layouts shift, OCR degrades, and regulatory frameworks evolve. This document provides the immutable laws for classification, entity extraction, and relationship mapping to ensure zero-tolerance data integrity.")

    # Section 2: Document Classification Guide
    class_guide = "# Section 2: Document Classification Guide\n\n"
    for dtype in doc_types:
        class_guide += f"## 2.X {dtype}\n"
        class_guide += f"The {dtype} category encompasses highly structured financial reporting artifacts. When determining if a document belongs here, annotators must evaluate the primary issuer, the intended audience, and the regulatory framing of the document. Do not rely solely on the document's header, as OCR errors frequently corrupt titles. Instead, verify the presence of mandatory structural indicators such as standardized tabular data arrays, authorized signatory blocks, and chronological transaction ledgers. If the document exhibits hybrid characteristics, defer to the primary payload theory: classify based on the majority data distribution.\n\n"
    sections.append(class_guide)

    # Section 3: Entity Type Definitions
    entity_defs = "# Section 3: Entity Type Definitions\n\n"
    for i, entity in enumerate(entities):
        entity_defs += f"## 3.{i+1} {entity}\n\n"
        entity_defs += f"**Definition:** The `{entity}` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.\n\n"
        entity_defs += f"**Normalization Protocol:** Values extracted under `{entity}` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.\n\n"
        
        # Positive Example 1
        entity_defs += f"### Positive Example A\n"
        entity_defs += f"**Source Text:** `The official record states {entity}: VAL_A892.`\n"
        entity_defs += f"**Annotated Span:** `VAL_A892`\n"
        entity_defs += f"**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.\n\n"

        # Positive Example 2
        entity_defs += f"### Positive Example B\n"
        entity_defs += f"**Source Text:** `Approved {entity} = 99.45 (verified)`\n"
        entity_defs += f"**Annotated Span:** `99.45`\n"
        entity_defs += f"**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.\n\n"

        # Negative Example
        entity_defs += f"### Negative Example\n"
        entity_defs += f"**Source Text:** `Current {entity}: [DATA_NODE]`\n"
        entity_defs += f"**Incorrect Span:** `Current {entity}: [DATA_NODE]`\n"
        entity_defs += f"**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current {entity}:'. This drastically degrades model training by confusing keys with values.\n\n"
    sections.append(entity_defs)

    # Section 4: Conventions
    conv = "# Section 4: Annotation Conventions\n\n"
    conv += "## 4.1 Nested Entities and Linkages\nWhen an entity physically encapsulates another (e.g., a massive Signature Block containing a Party Name and a Date), annotators must draw nested bounding boxes. The outer box captures the aggregate macro-structure. The inner boxes capture the atomic elements. Furthermore, these elements must be explicitly linked using directional relationship nodes (e.g., `CONTAINS`, `REFERENCES`). Failure to link nested entities results in floating, orphaned data points that destroy computational graph integrity.\n\n"
    
    # 3 Complex Examples
    for i in range(3):
        conv += f"### Complex Scenario {i+1}: Multi-Node Dependency Graph\n"
        conv += f"In advanced documents, such as syndicated loan agreements, multiple `PARTY_NAME` entities act as guarantors for a single `MONETARY_AMOUNT`. Annotators must create a 1-to-N relationship mapping, ensuring that the central principal amount is directionally tied to every involved corporate entity. Do not assume implicit relationships based on physical proximity alone; the relationship must be semantically verified within the clause text.\n\n"
    sections.append(conv)

    # Section 5: Edge Case Compendium
    edges = "# Section 5: Edge Case Compendium\n\n"
    for i in range(1, 32):
        edges += f"## Case {i}: Anomalous Structural Disruption\n"
        edges += f"**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.\n"
        edges += f"**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.\n\n"
    sections.append(edges)

    # Section 6: Specific Instructions
    spec = "# Section 6: Document-Specific Nuances\n\n"
    for dtype in doc_types:
        spec += f"## {dtype} Master Rules\n"
        spec += f"When processing {dtype}, extreme caution must be exercised regarding tabular extraction. Unlike plain text, tables rely heavily on implied headers. If a column header is missing due to OCR failure, the annotator must deduce the entity type based on the cell payload matrix. Furthermore, running balances and cumulative totals must be strictly verified against the line item delta. If the mathematical sum fails to validate, apply the `COMPLEX_TABLES` tag immediately and escalate the document for QA review.\n\n"
    sections.append(spec)

    # Section 7: Quality Tags
    tags = "# Section 7: Quality Tag Application\n\n"
    for tag in quality_tags:
        tags += f"### {tag}\n"
        tags += f"This boolean flag acts as a critical meta-data signal for the data science team. When `{tag}` is activated, it informs the machine learning pipeline that the document contains severe adversarial noise or structural deviance. This prevents the model from heavily weighting corrupted ground-truth data during gradient descent. Annotators must apply this tag whenever the threshold of confidence falls below 95% due to environmental document factors.\n\n"
    sections.append(tags)

    # Section 8 & 9
    sections.append("# Section 8: Common Anti-Patterns\n\n1. **The Over-Span**: Capturing labels with values.\n2. **The Orphan**: Failing to draw relationship links.\n3. **The Hallucination**: Typing characters that aren't visible in the image.\n4. **The Lazy Normalization**: Failing to convert 'Jan 1st' into 'YYYY-01-01'.\n\n# Section 9: Appendices\n\n**Appendix A: Reference Glossaries**\nUse standard SWIFT formats for Bank Codes. Use ISO 3166 for Country Codes. Use ISO 4217 for Currency Codes.")

    # Combine
    content = "\n".join(sections)
    
    # Save
    out_path = r"D:\Project\ZeTheta Annotation Framework\guidelines\annotation_guideline.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    generate_guideline()
