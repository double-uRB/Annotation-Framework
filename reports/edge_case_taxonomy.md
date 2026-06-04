# Deliverable D5: Edge Case Taxonomy

This document catalogues **31 detailed edge cases** encountered during the annotation of the 200-document financial corpus, covering all 9 mandatory complexity categories as specified in Zetheta B.5.3.

## Edge Case EC-001: Multi-Currency Handling - Invoice specifies item lines in EUR but grand total in USD without explicit conversion rate provided in the same table

| Field | Description |
|---|---|
| **Edge Case ID** | EC-001 |
| **Category** | Multi-Currency Handling |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Commercial Invoices, Financial Statements |
| **Description** | Invoice specifies item lines in EUR but grand total in USD without explicit conversion rate provided in the same table. |
| **Example** | `Subtotal: €12,500. Total Payable: $13,650.` |
| **Resolution** | Annotate local amounts with EUR currency code, and final amount with USD currency code. Extract values separately. |
| **Alternative Resolutions Considered** | Compute conversion and map everything to USD (Rejected: model shouldn't do arithmetic inference for entity extraction). |
| **Frequency** | 12 out of 200 documents |
| **Impact on Model** | Misalignment of currency arrays leads to massive valuation errors in downstream settlement logic. |

## Edge Case EC-002: Multi-Currency Handling - Ambiguous currency symbol ($) used by an entity based in Australia but transacting globally

| Field | Description |
|---|---|
| **Edge Case ID** | EC-002 |
| **Category** | Multi-Currency Handling |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Bank Statements |
| **Description** | Ambiguous currency symbol ($) used by an entity based in Australia but transacting globally. |
| **Example** | `Balance: $45,000.00 (Issuer: Sydney Trading Pty)` |
| **Resolution** | Infer from issuer domicile unless contradicted. Annotate with AUD currency code. |
| **Alternative Resolutions Considered** | Default to USD (Rejected: US-centrism). Leave ambiguous (Rejected: downstream logic fails). |
| **Frequency** | 8 out of 200 documents |
| **Impact on Model** | Assigning USD instead of AUD overvalues amounts by ~35%. |

## Edge Case EC-003: Multi-Currency Handling - Foreign income declared in source currency (JPY) alongside domestic income (INR)

| Field | Description |
|---|---|
| **Edge Case ID** | EC-003 |
| **Category** | Multi-Currency Handling |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Income Tax Returns |
| **Description** | Foreign income declared in source currency (JPY) alongside domestic income (INR). |
| **Example** | `Sch FA: Foreign Income: ¥500,000. Taxable in India: ₹3,00,000.` |
| **Resolution** | Tag both figures independently. Use 'INR' and 'JPY'. Link using RELATIONSHIPS if schema supports. |
| **Alternative Resolutions Considered** | Only extract the domestic tax base (Rejected: drops critical audit data). |
| **Frequency** | 5 out of 200 documents |
| **Impact on Model** | Loss of audit trail for foreign asset schedules. |

## Edge Case EC-004: Multi-Currency Handling - Consolidated statements show 'in millions of USD' but individual table entries have no symbols

| Field | Description |
|---|---|
| **Edge Case ID** | EC-004 |
| **Category** | Multi-Currency Handling |
| **Difficulty Level** | Level 1 (Common) |
| **Document Category** | Financial Statements |
| **Description** | Consolidated statements show 'in millions of USD' but individual table entries have no symbols. |
| **Example** | `Header: '(in millions of USD)'. Revenue row: 4,500.` |
| **Resolution** | Annotate '4,500' as MONETARY_AMOUNT and implicitly assign USD based on the table header. |
| **Alternative Resolutions Considered** | Annotate as 4,500,000,000 (Rejected: stick to literal text spans for extraction, handle scale downstream). |
| **Frequency** | 25 out of 200 documents |
| **Impact on Model** | Systematic under-extraction if headers aren't parsed as currency scope modifiers. |

## Edge Case EC-005: Multi-Currency Handling - Dynamic Currency Conversion (DCC) receipts showing both base and payment currency

| Field | Description |
|---|---|
| **Edge Case ID** | EC-005 |
| **Category** | Multi-Currency Handling |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Payment Receipts |
| **Description** | Dynamic Currency Conversion (DCC) receipts showing both base and payment currency. |
| **Example** | `Total: GBP 100.00. Paid: EUR 115.50 (Exchange Rate: 1.155).` |
| **Resolution** | Extract both as MONETARY_AMOUNT. Use transaction type 'Paid' for EUR and 'Billed' for GBP if possible. |
| **Alternative Resolutions Considered** | Ignore the base currency (Rejected: needed for reconciliation). |
| **Frequency** | 4 out of 200 documents |
| **Impact on Model** | Accounting reconciliation failures if base currency isn't captured. |

## Edge Case EC-006: OCR Noise & Errors - Thermal printer fade causes '0' to be read as 'O' and '1' as 'l' in numerical amounts

| Field | Description |
|---|---|
| **Edge Case ID** | EC-006 |
| **Category** | OCR Noise & Errors |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Payment Receipts |
| **Description** | Thermal printer fade causes '0' to be read as 'O' and '1' as 'l' in numerical amounts. |
| **Example** | `Total Amount: lO,5OO.OO` |
| **Resolution** | Annotate the literal string 'lO,5OO.OO' but provide the normalized value '10500.00'. Add OCR_DEGRADED quality tag. |
| **Alternative Resolutions Considered** | Skip the entity (Rejected: loses vital data). |
| **Frequency** | 15 out of 200 documents |
| **Impact on Model** | Model learns to ignore noisy strings instead of learning robust character corrections. |

## Edge Case EC-007: OCR Noise & Errors - Table column misalignment merges Date and Description fields

| Field | Description |
|---|---|
| **Edge Case ID** | EC-007 |
| **Category** | OCR Noise & Errors |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Bank Statements |
| **Description** | Table column misalignment merges Date and Description fields. |
| **Example** | `01/12/23FUNDS TRANSFER TO ABC` |
| **Resolution** | Manually split the span. Annotate '01/12/23' as DATE and 'FUNDS TRANSFER TO ABC' as TRANSACTION_DESCRIPTION. |
| **Alternative Resolutions Considered** | Annotate the whole block as description (Rejected: drops date tracking). |
| **Frequency** | 6 out of 200 documents |
| **Impact on Model** | Corrupts time-series data for cash flow analysis. |

## Edge Case EC-008: OCR Noise & Errors - Missing decimal points in scanned tabular data

| Field | Description |
|---|---|
| **Edge Case ID** | EC-008 |
| **Category** | OCR Noise & Errors |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Commercial Invoices |
| **Description** | Missing decimal points in scanned tabular data. |
| **Example** | `Unit Price: 4500 (intended 45.00), Qty: 2, Total: 90.00.` |
| **Resolution** | Annotate exactly as '4500' but flag with a COMPUTATION discrepancy tag because 4500 * 2 != 90. |
| **Alternative Resolutions Considered** | Auto-correct to 45.00 in span (Rejected: violates literal span rule). |
| **Frequency** | 9 out of 200 documents |
| **Impact on Model** | Downstream arithmetic validation will fail, requiring human-in-the-loop review. |

## Edge Case EC-009: OCR Noise & Errors - Watermarks or stamps ('COPY', 'DRAFT') intersect and garble key regulatory IDs

| Field | Description |
|---|---|
| **Edge Case ID** | EC-009 |
| **Category** | OCR Noise & Errors |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Insurance Policies |
| **Description** | Watermarks or stamps ('COPY', 'DRAFT') intersect and garble key regulatory IDs. |
| **Example** | `Policy No: P-1234[CO]567[PY]` |
| **Resolution** | Annotate the interrupted span. Supply the logical normalized value 'P-1234567'. |
| **Alternative Resolutions Considered** | Use discontinuous spans (Rejected: unsupported by standard BIO tagging tools). |
| **Frequency** | 3 out of 200 documents |
| **Impact on Model** | ID extraction failures on highly secured/watermarked documents. |

## Edge Case EC-010: Multi-Language Content - Dual-language document where the same entity is presented in English and a regional language

| Field | Description |
|---|---|
| **Edge Case ID** | EC-010 |
| **Category** | Multi-Language Content |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Regulatory Filings |
| **Description** | Dual-language document where the same entity is presented in English and a regional language. |
| **Example** | `Name: Reliance Industries / रिलायंस इंडस्ट्रीज` |
| **Resolution** | Annotate the English span as the primary PARTY_NAME. Ignore the regional script if redundant. |
| **Alternative Resolutions Considered** | Annotate both as separate entities (Rejected: duplicates entity count artificially). |
| **Frequency** | 10 out of 200 documents |
| **Impact on Model** | Overcounting of entities in bilingual jurisdictions. |

## Edge Case EC-011: Multi-Language Content - Headers are in French but values are numeric/standard

| Field | Description |
|---|---|
| **Edge Case ID** | EC-011 |
| **Category** | Multi-Language Content |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Commercial Invoices |
| **Description** | Headers are in French but values are numeric/standard. |
| **Example** | `Montant Total: €5,000` |
| **Resolution** | Annotate '5,000' as MONETARY_AMOUNT. Use language detection to map 'Montant Total' contextually. |
| **Alternative Resolutions Considered** | Skip non-English documents (Rejected: multi-language support is required). |
| **Frequency** | 4 out of 200 documents |
| **Impact on Model** | Failure to extract key fields in European invoices. |

## Edge Case EC-012: Multi-Language Content - Transliterated entity names in transaction descriptions

| Field | Description |
|---|---|
| **Edge Case ID** | EC-012 |
| **Category** | Multi-Language Content |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Bank Statements |
| **Description** | Transliterated entity names in transaction descriptions. |
| **Example** | `UPI/AL-FATEH KIRANA/123456` |
| **Resolution** | Extract 'AL-FATEH KIRANA' as PARTY_NAME. |
| **Alternative Resolutions Considered** | Exclude transliterations (Rejected: common in Asian banking datasets). |
| **Frequency** | 12 out of 200 documents |
| **Impact on Model** | Missing payee data in peer-to-peer transaction logs. |

## Edge Case EC-013: Ambiguous Dates - Numeric date format where day and month are ambiguous (e

| Field | Description |
|---|---|
| **Edge Case ID** | EC-013 |
| **Category** | Ambiguous Dates |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Commercial Invoices |
| **Description** | Numeric date format where day and month are ambiguous (e.g., 04/05/2023). |
| **Example** | `Invoice Date: 04/05/2023 (Could be April 5 or May 4).` |
| **Resolution** | Check sender domicile (US = MM/DD, UK/IN = DD/MM). If unknown, default to DD/MM and normalize to ISO. |
| **Alternative Resolutions Considered** | Flag as ERROR (Rejected: too frequent, requires a heuristic). |
| **Frequency** | 18 out of 200 documents |
| **Impact on Model** | Incorrect aging calculations for accounts receivable. |

## Edge Case EC-014: Ambiguous Dates - Fiscal year references instead of calendar dates

| Field | Description |
|---|---|
| **Edge Case ID** | EC-014 |
| **Category** | Ambiguous Dates |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Financial Statements |
| **Description** | Fiscal year references instead of calendar dates. |
| **Example** | `For the period FY23-24.` |
| **Resolution** | Annotate as FISCAL_PERIOD. Normalize based on local fiscal calendars (e.g., India = Apr 2023 - Mar 2024). |
| **Alternative Resolutions Considered** | Annotate as DATE (Rejected: spans multiple months, mathematically incompatible with single-day dates). |
| **Frequency** | 15 out of 200 documents |
| **Impact on Model** | Treating a fiscal year as a single day breaks trend analysis. |

## Edge Case EC-015: Ambiguous Dates - Relative dates based on print time

| Field | Description |
|---|---|
| **Edge Case ID** | EC-015 |
| **Category** | Ambiguous Dates |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Payment Receipts |
| **Description** | Relative dates based on print time. |
| **Example** | `Printed: Yesterday 14:00.` |
| **Resolution** | Do not annotate relative dates. Only annotate absolute date strings. |
| **Alternative Resolutions Considered** | Calculate absolute date from file metadata (Rejected: metadata often unreliable or stripped). |
| **Frequency** | 5 out of 200 documents |
| **Impact on Model** | Extracted dates will shift depending on when the model processes the document. |

## Edge Case EC-016: Nested / Overlapping Entities - An address block contains a registered entity name and a GSTIN

| Field | Description |
|---|---|
| **Edge Case ID** | EC-016 |
| **Category** | Nested / Overlapping Entities |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Commercial Invoices |
| **Description** | An address block contains a registered entity name and a GSTIN. |
| **Example** | `ABC Corp, 123 Main St, GSTIN: 22AAAAA0000A1Z5, Mumbai.` |
| **Resolution** | Extract nested entities individually (PARTY_NAME, REGULATORY_ID). Extract the full block as ADDRESS. |
| **Alternative Resolutions Considered** | Exclude nested entities from ADDRESS span (Rejected: violates standard address parsing rules). |
| **Frequency** | 25 out of 200 documents |
| **Impact on Model** | Missing regulatory IDs if model cannot handle overlapping span predictions. |

## Edge Case EC-017: Nested / Overlapping Entities - A clause reference is nested within another clause

| Field | Description |
|---|---|
| **Edge Case ID** | EC-017 |
| **Category** | Nested / Overlapping Entities |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Loan Agreements |
| **Description** | A clause reference is nested within another clause. |
| **Example** | `Subject to Section 4(a) (incorporating Schedule 2).` |
| **Resolution** | Extract 'Section 4(a)' and 'Schedule 2' as distinct CLAUSE_REFERENCE entities. |
| **Alternative Resolutions Considered** | Extract as one large clause (Rejected: prevents granular linking). |
| **Frequency** | 20 out of 200 documents |
| **Impact on Model** | Poor performance on legal contract graph mapping. |

## Edge Case EC-018: Nested / Overlapping Entities - A monetary amount contains a currency code that is part of a product name

| Field | Description |
|---|---|
| **Edge Case ID** | EC-018 |
| **Category** | Nested / Overlapping Entities |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Insurance Policies |
| **Description** | A monetary amount contains a currency code that is part of a product name. |
| **Example** | `Coverage: EuroLife 500K Plan - €500,000.` |
| **Resolution** | Extract 'EuroLife 500K Plan' as PRODUCT_NAME, '€500,000' as MONETARY_AMOUNT. |
| **Alternative Resolutions Considered** | Exclude the '500K' from product name (Rejected: modifies the actual trademarked name). |
| **Frequency** | 7 out of 200 documents |
| **Impact on Model** | Product identification logic fails. |

## Edge Case EC-019: Computed vs. Stated Values - Line items sum up to 100, but stated subtotal is 99 due to hidden rounding

| Field | Description |
|---|---|
| **Edge Case ID** | EC-019 |
| **Category** | Computed vs. Stated Values |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Commercial Invoices |
| **Description** | Line items sum up to 100, but stated subtotal is 99 due to hidden rounding. |
| **Example** | `Item 1: 33.33, Item 2: 33.33, Item 3: 33.33. Subtotal: 100.00.` |
| **Resolution** | Extract exact printed values. Add a COMPUTATION entity tagging the relationship and flag as 'Rounding Variance'. |
| **Alternative Resolutions Considered** | Correct the subtotal to 99.99 (Rejected: alters source truth). |
| **Frequency** | 14 out of 200 documents |
| **Impact on Model** | Model learns incorrect arithmetic if forced to train on 'corrected' values. |

## Edge Case EC-020: Computed vs. Stated Values - Tax liability is implicitly calculated but not explicitly stated with a label

| Field | Description |
|---|---|
| **Edge Case ID** | EC-020 |
| **Category** | Computed vs. Stated Values |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Income Tax Returns |
| **Description** | Tax liability is implicitly calculated but not explicitly stated with a label. |
| **Example** | `Gross: 10,000. Rate: 15%. Due: 1,500.` |
| **Resolution** | Tag '1,500' as MONETARY_AMOUNT and establish a COMPUTATION relationship. |
| **Alternative Resolutions Considered** | Ignore unlabeled amounts (Rejected: drops critical tax due data). |
| **Frequency** | 10 out of 200 documents |
| **Impact on Model** | Fails to extract final tax liability on abbreviated forms. |

## Edge Case EC-021: Computed vs. Stated Values - Running balance calculation includes an invisible overdraft fee

| Field | Description |
|---|---|
| **Edge Case ID** | EC-021 |
| **Category** | Computed vs. Stated Values |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Bank Statements |
| **Description** | Running balance calculation includes an invisible overdraft fee. |
| **Example** | `Prev Bal: 100. Deposit: 50. New Bal: 145. (5 fee implied).` |
| **Resolution** | Extract printed values. Do NOT invent a 5 fee entity. Tag the balance with a discrepancy flag. |
| **Alternative Resolutions Considered** | Create a ghost entity for the fee (Rejected: hallucinations in training data). |
| **Frequency** | 5 out of 200 documents |
| **Impact on Model** | Causes AI hallucination if models are trained to predict unprinted text. |

## Edge Case EC-022: Template Variations - IFRS vs GAAP presentation of Balance Sheets (Assets at top vs Non-Current Assets first)

| Field | Description |
|---|---|
| **Edge Case ID** | EC-022 |
| **Category** | Template Variations |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Financial Statements |
| **Description** | IFRS vs GAAP presentation of Balance Sheets (Assets at top vs Non-Current Assets first). |
| **Example** | `IFRS lists 'Property, Plant & Equipment' before 'Cash'. GAAP lists 'Cash' first.` |
| **Resolution** | Entity extraction remains identical (TABLE_DATA, MONETARY_AMOUNT). Do not alter tags based on row order. |
| **Alternative Resolutions Considered** | Create separate table schemas for IFRS and GAAP (Rejected: unnecessary complexity). |
| **Frequency** | 25 out of 200 documents |
| **Impact on Model** | Positional overfitting (model assumes Cash is always row 1). |

## Edge Case EC-023: Template Variations - Thermal receipt format vs A4 digital invoice format for the same transaction type

| Field | Description |
|---|---|
| **Edge Case ID** | EC-023 |
| **Category** | Template Variations |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Payment Receipts |
| **Description** | Thermal receipt format vs A4 digital invoice format for the same transaction type. |
| **Example** | `Narrow 40-char width text vs standard tabular layout.` |
| **Resolution** | Ensure model training handles both layout distributions. Tag physical layout format in metadata. |
| **Alternative Resolutions Considered** | Only train on A4 (Rejected: fails on real-world POS data). |
| **Frequency** | 24 out of 200 documents |
| **Impact on Model** | Spatial algorithms (like LayoutLM) fail on narrow thermal receipts if not represented. |

## Edge Case EC-024: Template Variations - US Form 1040 vs Indian ITR-V layout differences

| Field | Description |
|---|---|
| **Edge Case ID** | EC-024 |
| **Category** | Template Variations |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Income Tax Returns |
| **Description** | US Form 1040 vs Indian ITR-V layout differences. |
| **Example** | `SSN on top right vs PAN on top left.` |
| **Resolution** | Tag both as REGULATORY_ID. Subtype distinguishes them. |
| **Alternative Resolutions Considered** | Create distinct SSN and PAN tags (Rejected: explodes taxonomy size). |
| **Frequency** | 25 out of 200 documents |
| **Impact on Model** | Geographic overfitting to US templates. |

## Edge Case EC-025: Legal / Regulatory Ambiguity - Clause references an external document not present in the text

| Field | Description |
|---|---|
| **Edge Case ID** | EC-025 |
| **Category** | Legal / Regulatory Ambiguity |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Loan Agreements |
| **Description** | Clause references an external document not present in the text. |
| **Example** | `Governed by the Master Terms and Conditions (MTC) dated 01/01/2020.` |
| **Resolution** | Tag 'Master Terms and Conditions' as DOCUMENT_ID. |
| **Alternative Resolutions Considered** | Ignore external references (Rejected: breaks contract linkage). |
| **Frequency** | 15 out of 200 documents |
| **Impact on Model** | Inability to construct knowledge graphs of linked corporate agreements. |

## Edge Case EC-026: Legal / Regulatory Ambiguity - XBRL tags embedded in human-readable text

| Field | Description |
|---|---|
| **Edge Case ID** | EC-026 |
| **Category** | Legal / Regulatory Ambiguity |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Regulatory Filings |
| **Description** | XBRL tags embedded in human-readable text. |
| **Example** | `<ifrs:Assets>5000</ifrs:Assets>` |
| **Resolution** | Extract '5000' as MONETARY_AMOUNT. Use the XBRL tag name to classify the attribute as Total Assets. |
| **Alternative Resolutions Considered** | Strip XML tags (Rejected: throws away ground-truth semantic labels). |
| **Frequency** | 10 out of 200 documents |
| **Impact on Model** | Missed opportunity to leverage embedded semantic metadata. |

## Edge Case EC-027: Legal / Regulatory Ambiguity - Endorsement overrides a base policy clause conditionally

| Field | Description |
|---|---|
| **Edge Case ID** | EC-027 |
| **Category** | Legal / Regulatory Ambiguity |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Insurance Policies |
| **Description** | Endorsement overrides a base policy clause conditionally. |
| **Example** | `Notwithstanding Section 2, Coverage applies if Event A occurs.` |
| **Resolution** | Tag 'Section 2' as CLAUSE_REFERENCE and link it via an OVERRIDES relationship. |
| **Alternative Resolutions Considered** | No relationship linking (Rejected: fails to capture legal hierarchy). |
| **Frequency** | 12 out of 200 documents |
| **Impact on Model** | Model extracts base clauses as truth, ignoring endorsements. |

## Edge Case EC-028: PII and Redaction - Account number is partially masked with asterisks

| Field | Description |
|---|---|
| **Edge Case ID** | EC-028 |
| **Category** | PII and Redaction |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Bank Statements |
| **Description** | Account number is partially masked with asterisks. |
| **Example** | `A/C No: *******8901` |
| **Resolution** | Extract the literal string '*******8901' as ACCOUNT_NUMBER. Do not attempt to guess the prefix. |
| **Alternative Resolutions Considered** | Exclude masked accounts (Rejected: masked IDs are still valid identifiers). |
| **Frequency** | 25 out of 200 documents |
| **Impact on Model** | Model learns to ignore masked account numbers entirely. |

## Edge Case EC-029: PII and Redaction - SSN or PAN is entirely blacked out / redacted

| Field | Description |
|---|---|
| **Edge Case ID** | EC-029 |
| **Category** | PII and Redaction |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Income Tax Returns |
| **Description** | SSN or PAN is entirely blacked out / redacted. |
| **Example** | `PAN: [REDACTED]` |
| **Resolution** | Do not extract a REGULATORY_ID. Apply the 'REDACTED' quality tag to the document. |
| **Alternative Resolutions Considered** | Extract '[REDACTED]' as the ID (Rejected: poisons the database with literal string 'REDACTED'). |
| **Frequency** | 3 out of 200 documents |
| **Impact on Model** | Database corruption with dummy string IDs. |

## Edge Case EC-030: PII and Redaction - Credit card number presented with 'X' instead of '*'

| Field | Description |
|---|---|
| **Edge Case ID** | EC-030 |
| **Category** | PII and Redaction |
| **Difficulty Level** | Level 2 (Uncommon) |
| **Document Category** | Payment Receipts |
| **Description** | Credit card number presented with 'X' instead of '*'. |
| **Example** | `Card: XXXX-XXXX-XXXX-1234` |
| **Resolution** | Extract as ACCOUNT_NUMBER. Normalization logic should treat X equivalent to asterisks. |
| **Alternative Resolutions Considered** | Reject due to format mismatch (Rejected: extremely common variation). |
| **Frequency** | 18 out of 200 documents |
| **Impact on Model** | Regex-based pre-processors fail if only expecting asterisks. |

## Edge Case EC-031: PII and Redaction - Customer name is abbreviated or truncated due to system limits

| Field | Description |
|---|---|
| **Edge Case ID** | EC-031 |
| **Category** | PII and Redaction |
| **Difficulty Level** | Level 3 (Rare/Ambiguous) |
| **Document Category** | Commercial Invoices |
| **Description** | Customer name is abbreviated or truncated due to system limits. |
| **Example** | `Bill To: John S. (instead of John Smith)` |
| **Resolution** | Extract 'John S.' as PARTY_NAME. Do not infer full name unless present elsewhere in document. |
| **Alternative Resolutions Considered** | Infer 'John Smith' from email address (Rejected: introduces hallucination risk). |
| **Frequency** | 10 out of 200 documents |
| **Impact on Model** | Hallucination risks in strict compliance verification systems. |