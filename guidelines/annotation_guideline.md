# Section 1: Introduction & Purpose

This Annotation Guideline serves as the definitive master reference for the FinSight AI project. It establishes the rigid boundaries, taxonomy definitions, and procedural workflows necessary to extract structured financial data from deeply unstructured, multi-modal documents. The success of the downstream predictive models relies entirely on strict adherence to these rules.

Annotators must understand that financial documents are inherently adversarial. They are designed for human readability, not machine parsing. Layouts shift, OCR degrades, and regulatory frameworks evolve. This document provides the immutable laws for classification, entity extraction, and relationship mapping to ensure zero-tolerance data integrity.
# Section 2: Document Classification Guide

## 2.X Bank Statements
The Bank Statements category encompasses highly structured financial reporting artifacts. When determining if a document belongs here, annotators must evaluate the primary issuer, the intended audience, and the regulatory framing of the document. Do not rely solely on the document's header, as OCR errors frequently corrupt titles. Instead, verify the presence of mandatory structural indicators such as standardized tabular data arrays, authorized signatory blocks, and chronological transaction ledgers. If the document exhibits hybrid characteristics, defer to the primary payload theory: classify based on the majority data distribution.

## 2.X Invoices & Receipts
The Invoices & Receipts category encompasses highly structured financial reporting artifacts. When determining if a document belongs here, annotators must evaluate the primary issuer, the intended audience, and the regulatory framing of the document. Do not rely solely on the document's header, as OCR errors frequently corrupt titles. Instead, verify the presence of mandatory structural indicators such as standardized tabular data arrays, authorized signatory blocks, and chronological transaction ledgers. If the document exhibits hybrid characteristics, defer to the primary payload theory: classify based on the majority data distribution.

## 2.X Tax Returns
The Tax Returns category encompasses highly structured financial reporting artifacts. When determining if a document belongs here, annotators must evaluate the primary issuer, the intended audience, and the regulatory framing of the document. Do not rely solely on the document's header, as OCR errors frequently corrupt titles. Instead, verify the presence of mandatory structural indicators such as standardized tabular data arrays, authorized signatory blocks, and chronological transaction ledgers. If the document exhibits hybrid characteristics, defer to the primary payload theory: classify based on the majority data distribution.

## 2.X Loan Agreements
The Loan Agreements category encompasses highly structured financial reporting artifacts. When determining if a document belongs here, annotators must evaluate the primary issuer, the intended audience, and the regulatory framing of the document. Do not rely solely on the document's header, as OCR errors frequently corrupt titles. Instead, verify the presence of mandatory structural indicators such as standardized tabular data arrays, authorized signatory blocks, and chronological transaction ledgers. If the document exhibits hybrid characteristics, defer to the primary payload theory: classify based on the majority data distribution.

## 2.X Insurance Policies
The Insurance Policies category encompasses highly structured financial reporting artifacts. When determining if a document belongs here, annotators must evaluate the primary issuer, the intended audience, and the regulatory framing of the document. Do not rely solely on the document's header, as OCR errors frequently corrupt titles. Instead, verify the presence of mandatory structural indicators such as standardized tabular data arrays, authorized signatory blocks, and chronological transaction ledgers. If the document exhibits hybrid characteristics, defer to the primary payload theory: classify based on the majority data distribution.

## 2.X Regulatory Filings
The Regulatory Filings category encompasses highly structured financial reporting artifacts. When determining if a document belongs here, annotators must evaluate the primary issuer, the intended audience, and the regulatory framing of the document. Do not rely solely on the document's header, as OCR errors frequently corrupt titles. Instead, verify the presence of mandatory structural indicators such as standardized tabular data arrays, authorized signatory blocks, and chronological transaction ledgers. If the document exhibits hybrid characteristics, defer to the primary payload theory: classify based on the majority data distribution.

## 2.X Payment Receipts
The Payment Receipts category encompasses highly structured financial reporting artifacts. When determining if a document belongs here, annotators must evaluate the primary issuer, the intended audience, and the regulatory framing of the document. Do not rely solely on the document's header, as OCR errors frequently corrupt titles. Instead, verify the presence of mandatory structural indicators such as standardized tabular data arrays, authorized signatory blocks, and chronological transaction ledgers. If the document exhibits hybrid characteristics, defer to the primary payload theory: classify based on the majority data distribution.

## 2.X Financial Statements
The Financial Statements category encompasses highly structured financial reporting artifacts. When determining if a document belongs here, annotators must evaluate the primary issuer, the intended audience, and the regulatory framing of the document. Do not rely solely on the document's header, as OCR errors frequently corrupt titles. Instead, verify the presence of mandatory structural indicators such as standardized tabular data arrays, authorized signatory blocks, and chronological transaction ledgers. If the document exhibits hybrid characteristics, defer to the primary payload theory: classify based on the majority data distribution.


# Section 3: Entity Type Definitions

## 3.1 DOCUMENT_ID

**Definition:** The `DOCUMENT_ID` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `DOCUMENT_ID` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states DOCUMENT_ID: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved DOCUMENT_ID = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current DOCUMENT_ID: [DATA_NODE]`
**Incorrect Span:** `Current DOCUMENT_ID: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current DOCUMENT_ID:'. This drastically degrades model training by confusing keys with values.

## 3.2 DATE

**Definition:** The `DATE` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `DATE` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states DATE: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved DATE = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current DATE: [DATA_NODE]`
**Incorrect Span:** `Current DATE: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current DATE:'. This drastically degrades model training by confusing keys with values.

## 3.3 MONETARY_AMOUNT

**Definition:** The `MONETARY_AMOUNT` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `MONETARY_AMOUNT` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states MONETARY_AMOUNT: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved MONETARY_AMOUNT = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current MONETARY_AMOUNT: [DATA_NODE]`
**Incorrect Span:** `Current MONETARY_AMOUNT: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current MONETARY_AMOUNT:'. This drastically degrades model training by confusing keys with values.

## 3.4 PARTY_NAME

**Definition:** The `PARTY_NAME` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `PARTY_NAME` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states PARTY_NAME: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved PARTY_NAME = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current PARTY_NAME: [DATA_NODE]`
**Incorrect Span:** `Current PARTY_NAME: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current PARTY_NAME:'. This drastically degrades model training by confusing keys with values.

## 3.5 REGULATORY_ID

**Definition:** The `REGULATORY_ID` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `REGULATORY_ID` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states REGULATORY_ID: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved REGULATORY_ID = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current REGULATORY_ID: [DATA_NODE]`
**Incorrect Span:** `Current REGULATORY_ID: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current REGULATORY_ID:'. This drastically degrades model training by confusing keys with values.

## 3.6 ADDRESS

**Definition:** The `ADDRESS` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `ADDRESS` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states ADDRESS: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved ADDRESS = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current ADDRESS: [DATA_NODE]`
**Incorrect Span:** `Current ADDRESS: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current ADDRESS:'. This drastically degrades model training by confusing keys with values.

## 3.7 LINE_ITEM

**Definition:** The `LINE_ITEM` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `LINE_ITEM` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states LINE_ITEM: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved LINE_ITEM = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current LINE_ITEM: [DATA_NODE]`
**Incorrect Span:** `Current LINE_ITEM: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current LINE_ITEM:'. This drastically degrades model training by confusing keys with values.

## 3.8 COMPUTATION

**Definition:** The `COMPUTATION` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `COMPUTATION` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states COMPUTATION: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved COMPUTATION = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current COMPUTATION: [DATA_NODE]`
**Incorrect Span:** `Current COMPUTATION: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current COMPUTATION:'. This drastically degrades model training by confusing keys with values.

## 3.9 CLAUSE_REFERENCE

**Definition:** The `CLAUSE_REFERENCE` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `CLAUSE_REFERENCE` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states CLAUSE_REFERENCE: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved CLAUSE_REFERENCE = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current CLAUSE_REFERENCE: [DATA_NODE]`
**Incorrect Span:** `Current CLAUSE_REFERENCE: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current CLAUSE_REFERENCE:'. This drastically degrades model training by confusing keys with values.

## 3.10 SIGNATURE_BLOCK

**Definition:** The `SIGNATURE_BLOCK` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `SIGNATURE_BLOCK` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states SIGNATURE_BLOCK: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved SIGNATURE_BLOCK = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current SIGNATURE_BLOCK: [DATA_NODE]`
**Incorrect Span:** `Current SIGNATURE_BLOCK: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current SIGNATURE_BLOCK:'. This drastically degrades model training by confusing keys with values.

## 3.11 PERCENTAGE

**Definition:** The `PERCENTAGE` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `PERCENTAGE` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states PERCENTAGE: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved PERCENTAGE = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current PERCENTAGE: [DATA_NODE]`
**Incorrect Span:** `Current PERCENTAGE: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current PERCENTAGE:'. This drastically degrades model training by confusing keys with values.

## 3.12 TRANSACTION_TYPE

**Definition:** The `TRANSACTION_TYPE` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `TRANSACTION_TYPE` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states TRANSACTION_TYPE: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved TRANSACTION_TYPE = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current TRANSACTION_TYPE: [DATA_NODE]`
**Incorrect Span:** `Current TRANSACTION_TYPE: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current TRANSACTION_TYPE:'. This drastically degrades model training by confusing keys with values.

## 3.13 STATUS

**Definition:** The `STATUS` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `STATUS` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states STATUS: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved STATUS = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current STATUS: [DATA_NODE]`
**Incorrect Span:** `Current STATUS: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current STATUS:'. This drastically degrades model training by confusing keys with values.

## 3.14 ACCOUNT_NUMBER

**Definition:** The `ACCOUNT_NUMBER` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `ACCOUNT_NUMBER` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states ACCOUNT_NUMBER: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved ACCOUNT_NUMBER = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current ACCOUNT_NUMBER: [DATA_NODE]`
**Incorrect Span:** `Current ACCOUNT_NUMBER: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current ACCOUNT_NUMBER:'. This drastically degrades model training by confusing keys with values.

## 3.15 BANK_CODE

**Definition:** The `BANK_CODE` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `BANK_CODE` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states BANK_CODE: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved BANK_CODE = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current BANK_CODE: [DATA_NODE]`
**Incorrect Span:** `Current BANK_CODE: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current BANK_CODE:'. This drastically degrades model training by confusing keys with values.

## 3.16 CURRENCY_CODE

**Definition:** The `CURRENCY_CODE` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `CURRENCY_CODE` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states CURRENCY_CODE: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved CURRENCY_CODE = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current CURRENCY_CODE: [DATA_NODE]`
**Incorrect Span:** `Current CURRENCY_CODE: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current CURRENCY_CODE:'. This drastically degrades model training by confusing keys with values.

## 3.17 PHONE_NUMBER

**Definition:** The `PHONE_NUMBER` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `PHONE_NUMBER` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states PHONE_NUMBER: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved PHONE_NUMBER = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current PHONE_NUMBER: [DATA_NODE]`
**Incorrect Span:** `Current PHONE_NUMBER: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current PHONE_NUMBER:'. This drastically degrades model training by confusing keys with values.

## 3.18 EMAIL_ADDRESS

**Definition:** The `EMAIL_ADDRESS` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `EMAIL_ADDRESS` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states EMAIL_ADDRESS: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved EMAIL_ADDRESS = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current EMAIL_ADDRESS: [DATA_NODE]`
**Incorrect Span:** `Current EMAIL_ADDRESS: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current EMAIL_ADDRESS:'. This drastically degrades model training by confusing keys with values.

## 3.19 WEBSITE

**Definition:** The `WEBSITE` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `WEBSITE` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states WEBSITE: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved WEBSITE = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current WEBSITE: [DATA_NODE]`
**Incorrect Span:** `Current WEBSITE: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current WEBSITE:'. This drastically degrades model training by confusing keys with values.

## 3.20 TAX_CODE

**Definition:** The `TAX_CODE` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `TAX_CODE` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states TAX_CODE: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved TAX_CODE = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current TAX_CODE: [DATA_NODE]`
**Incorrect Span:** `Current TAX_CODE: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current TAX_CODE:'. This drastically degrades model training by confusing keys with values.

## 3.21 INTEREST_RATE

**Definition:** The `INTEREST_RATE` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `INTEREST_RATE` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states INTEREST_RATE: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved INTEREST_RATE = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current INTEREST_RATE: [DATA_NODE]`
**Incorrect Span:** `Current INTEREST_RATE: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current INTEREST_RATE:'. This drastically degrades model training by confusing keys with values.

## 3.22 DURATION

**Definition:** The `DURATION` entity represents a critical atomic unit of extraction. Annotators must isolate the strict minimal span containing the value, rigorously excluding any prefixed labels, trailing punctuation, or adjacent whitespace. Contextual identifiers such as 'Total:' or 'No.' must never be included in the bounding box.

**Normalization Protocol:** Values extracted under `DURATION` must be strictly cast to their canonical representations. Dates must resolve to ISO 8601 format (YYYY-MM-DD). Monetary amounts must be stripped of currency symbols and comma separators, yielding raw floating-point integers. Regulatory IDs must be formatted according to their issuing jurisdiction's exact spacing rules.

### Positive Example A
**Source Text:** `The official record states DURATION: VAL_A892.`
**Annotated Span:** `VAL_A892`
**Reasoning:** The span correctly isolates the payload from the surrounding boilerplate text and the colon separator.

### Positive Example B
**Source Text:** `Approved DURATION = 99.45 (verified)`
**Annotated Span:** `99.45`
**Reasoning:** The span successfully excludes the mathematical operator and the parenthetical verification stamp, strictly adhering to the minimal span doctrine.

### Negative Example
**Source Text:** `Current DURATION: [DATA_NODE]`
**Incorrect Span:** `Current DURATION: [DATA_NODE]`
**Reasoning:** The annotator committed an over-spanning violation by including the descriptive label 'Current DURATION:'. This drastically degrades model training by confusing keys with values.


# Section 4: Annotation Conventions

## 4.1 Nested Entities and Linkages
When an entity physically encapsulates another (e.g., a massive Signature Block containing a Party Name and a Date), annotators must draw nested bounding boxes. The outer box captures the aggregate macro-structure. The inner boxes capture the atomic elements. Furthermore, these elements must be explicitly linked using directional relationship nodes (e.g., `CONTAINS`, `REFERENCES`). Failure to link nested entities results in floating, orphaned data points that destroy computational graph integrity.

### Complex Scenario 1: Multi-Node Dependency Graph
In advanced documents, such as syndicated loan agreements, multiple `PARTY_NAME` entities act as guarantors for a single `MONETARY_AMOUNT`. Annotators must create a 1-to-N relationship mapping, ensuring that the central principal amount is directionally tied to every involved corporate entity. Do not assume implicit relationships based on physical proximity alone; the relationship must be semantically verified within the clause text.

### Complex Scenario 2: Multi-Node Dependency Graph
In advanced documents, such as syndicated loan agreements, multiple `PARTY_NAME` entities act as guarantors for a single `MONETARY_AMOUNT`. Annotators must create a 1-to-N relationship mapping, ensuring that the central principal amount is directionally tied to every involved corporate entity. Do not assume implicit relationships based on physical proximity alone; the relationship must be semantically verified within the clause text.

### Complex Scenario 3: Multi-Node Dependency Graph
In advanced documents, such as syndicated loan agreements, multiple `PARTY_NAME` entities act as guarantors for a single `MONETARY_AMOUNT`. Annotators must create a 1-to-N relationship mapping, ensuring that the central principal amount is directionally tied to every involved corporate entity. Do not assume implicit relationships based on physical proximity alone; the relationship must be semantically verified within the clause text.


# Section 5: Edge Case Compendium

## Case 1: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 2: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 3: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 4: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 5: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 6: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 7: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 8: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 9: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 10: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 11: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 12: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 13: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 14: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 15: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 16: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 17: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 18: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 19: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 20: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 21: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 22: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 23: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 24: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 25: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 26: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 27: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 28: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 29: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 30: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.

## Case 31: Anomalous Structural Disruption
**Observation:** During high-velocity batch processing, annotators frequently encounter documents where core components are misaligned, obfuscated by physical stamps, or fragmented across page breaks.
**Mandated Resolution:** Do not force-fit broken data into standard schemas. If a table spans two pages, annotate two distinct `TABLE_DATA` blocks and link them via `CONTINUATION_OF`. If a stamp obscures a `SIGNATURE_BLOCK`, annotate the visible span and apply the `STAMP_OBSCURATION` quality tag. Do not hallucinate occluded characters.


# Section 6: Document-Specific Nuances

## Bank Statements Master Rules
When processing Bank Statements, extreme caution must be exercised regarding tabular extraction. Unlike plain text, tables rely heavily on implied headers. If a column header is missing due to OCR failure, the annotator must deduce the entity type based on the cell payload matrix. Furthermore, running balances and cumulative totals must be strictly verified against the line item delta. If the mathematical sum fails to validate, apply the `COMPLEX_TABLES` tag immediately and escalate the document for QA review.

## Invoices & Receipts Master Rules
When processing Invoices & Receipts, extreme caution must be exercised regarding tabular extraction. Unlike plain text, tables rely heavily on implied headers. If a column header is missing due to OCR failure, the annotator must deduce the entity type based on the cell payload matrix. Furthermore, running balances and cumulative totals must be strictly verified against the line item delta. If the mathematical sum fails to validate, apply the `COMPLEX_TABLES` tag immediately and escalate the document for QA review.

## Tax Returns Master Rules
When processing Tax Returns, extreme caution must be exercised regarding tabular extraction. Unlike plain text, tables rely heavily on implied headers. If a column header is missing due to OCR failure, the annotator must deduce the entity type based on the cell payload matrix. Furthermore, running balances and cumulative totals must be strictly verified against the line item delta. If the mathematical sum fails to validate, apply the `COMPLEX_TABLES` tag immediately and escalate the document for QA review.

## Loan Agreements Master Rules
When processing Loan Agreements, extreme caution must be exercised regarding tabular extraction. Unlike plain text, tables rely heavily on implied headers. If a column header is missing due to OCR failure, the annotator must deduce the entity type based on the cell payload matrix. Furthermore, running balances and cumulative totals must be strictly verified against the line item delta. If the mathematical sum fails to validate, apply the `COMPLEX_TABLES` tag immediately and escalate the document for QA review.

## Insurance Policies Master Rules
When processing Insurance Policies, extreme caution must be exercised regarding tabular extraction. Unlike plain text, tables rely heavily on implied headers. If a column header is missing due to OCR failure, the annotator must deduce the entity type based on the cell payload matrix. Furthermore, running balances and cumulative totals must be strictly verified against the line item delta. If the mathematical sum fails to validate, apply the `COMPLEX_TABLES` tag immediately and escalate the document for QA review.

## Regulatory Filings Master Rules
When processing Regulatory Filings, extreme caution must be exercised regarding tabular extraction. Unlike plain text, tables rely heavily on implied headers. If a column header is missing due to OCR failure, the annotator must deduce the entity type based on the cell payload matrix. Furthermore, running balances and cumulative totals must be strictly verified against the line item delta. If the mathematical sum fails to validate, apply the `COMPLEX_TABLES` tag immediately and escalate the document for QA review.

## Payment Receipts Master Rules
When processing Payment Receipts, extreme caution must be exercised regarding tabular extraction. Unlike plain text, tables rely heavily on implied headers. If a column header is missing due to OCR failure, the annotator must deduce the entity type based on the cell payload matrix. Furthermore, running balances and cumulative totals must be strictly verified against the line item delta. If the mathematical sum fails to validate, apply the `COMPLEX_TABLES` tag immediately and escalate the document for QA review.

## Financial Statements Master Rules
When processing Financial Statements, extreme caution must be exercised regarding tabular extraction. Unlike plain text, tables rely heavily on implied headers. If a column header is missing due to OCR failure, the annotator must deduce the entity type based on the cell payload matrix. Furthermore, running balances and cumulative totals must be strictly verified against the line item delta. If the mathematical sum fails to validate, apply the `COMPLEX_TABLES` tag immediately and escalate the document for QA review.


# Section 7: Quality Tag Application

### OCR_DEGRADED
This boolean flag acts as a critical meta-data signal for the data science team. When `OCR_DEGRADED` is activated, it informs the machine learning pipeline that the document contains severe adversarial noise or structural deviance. This prevents the model from heavily weighting corrupted ground-truth data during gradient descent. Annotators must apply this tag whenever the threshold of confidence falls below 95% due to environmental document factors.

### HANDWRITTEN_ELEMENTS
This boolean flag acts as a critical meta-data signal for the data science team. When `HANDWRITTEN_ELEMENTS` is activated, it informs the machine learning pipeline that the document contains severe adversarial noise or structural deviance. This prevents the model from heavily weighting corrupted ground-truth data during gradient descent. Annotators must apply this tag whenever the threshold of confidence falls below 95% due to environmental document factors.

### MULTI_LANGUAGE
This boolean flag acts as a critical meta-data signal for the data science team. When `MULTI_LANGUAGE` is activated, it informs the machine learning pipeline that the document contains severe adversarial noise or structural deviance. This prevents the model from heavily weighting corrupted ground-truth data during gradient descent. Annotators must apply this tag whenever the threshold of confidence falls below 95% due to environmental document factors.

### MULTI_CURRENCY
This boolean flag acts as a critical meta-data signal for the data science team. When `MULTI_CURRENCY` is activated, it informs the machine learning pipeline that the document contains severe adversarial noise or structural deviance. This prevents the model from heavily weighting corrupted ground-truth data during gradient descent. Annotators must apply this tag whenever the threshold of confidence falls below 95% due to environmental document factors.

### COMPLEX_TABLES
This boolean flag acts as a critical meta-data signal for the data science team. When `COMPLEX_TABLES` is activated, it informs the machine learning pipeline that the document contains severe adversarial noise or structural deviance. This prevents the model from heavily weighting corrupted ground-truth data during gradient descent. Annotators must apply this tag whenever the threshold of confidence falls below 95% due to environmental document factors.

### POOR_CONTRAST
This boolean flag acts as a critical meta-data signal for the data science team. When `POOR_CONTRAST` is activated, it informs the machine learning pipeline that the document contains severe adversarial noise or structural deviance. This prevents the model from heavily weighting corrupted ground-truth data during gradient descent. Annotators must apply this tag whenever the threshold of confidence falls below 95% due to environmental document factors.

### MISSING_PAGES
This boolean flag acts as a critical meta-data signal for the data science team. When `MISSING_PAGES` is activated, it informs the machine learning pipeline that the document contains severe adversarial noise or structural deviance. This prevents the model from heavily weighting corrupted ground-truth data during gradient descent. Annotators must apply this tag whenever the threshold of confidence falls below 95% due to environmental document factors.

### SIGNATURE_OVERLAP
This boolean flag acts as a critical meta-data signal for the data science team. When `SIGNATURE_OVERLAP` is activated, it informs the machine learning pipeline that the document contains severe adversarial noise or structural deviance. This prevents the model from heavily weighting corrupted ground-truth data during gradient descent. Annotators must apply this tag whenever the threshold of confidence falls below 95% due to environmental document factors.

### STAMP_OBSCURATION
This boolean flag acts as a critical meta-data signal for the data science team. When `STAMP_OBSCURATION` is activated, it informs the machine learning pipeline that the document contains severe adversarial noise or structural deviance. This prevents the model from heavily weighting corrupted ground-truth data during gradient descent. Annotators must apply this tag whenever the threshold of confidence falls below 95% due to environmental document factors.

### NON_STANDARD_LAYOUT
This boolean flag acts as a critical meta-data signal for the data science team. When `NON_STANDARD_LAYOUT` is activated, it informs the machine learning pipeline that the document contains severe adversarial noise or structural deviance. This prevents the model from heavily weighting corrupted ground-truth data during gradient descent. Annotators must apply this tag whenever the threshold of confidence falls below 95% due to environmental document factors.


# Section 8: Common Anti-Patterns

1. **The Over-Span**: Capturing labels with values.
2. **The Orphan**: Failing to draw relationship links.
3. **The Hallucination**: Typing characters that aren't visible in the image.
4. **The Lazy Normalization**: Failing to convert 'Jan 1st' into 'YYYY-01-01'.

# Section 9: Appendices

**Appendix A: Reference Glossaries**
Use standard SWIFT formats for Bank Codes. Use ISO 3166 for Country Codes. Use ISO 4217 for Currency Codes.