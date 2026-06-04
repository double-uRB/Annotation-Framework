# Inter-Annotator Agreement (IAA) Mathematical Model & Codex Instructions

This document provides the formal architectural specification for the Inter-Annotator Agreement (IAA) pipeline. Codex must strictly implement these calculations in the final `scripts/compute_iaa.py`.

## 1. Classification Agreement: Cohen’s Kappa ($\kappa$)
For document-level classifications (Primary Category and Subtype), use Cohen’s Kappa to adjust for chance agreement.

**Mathematical Definition:**
$$\kappa = \frac{p_o - p_e}{1 - p_e}$$
- **$p_o$**: Relative observed agreement among raters.
- **$p_e$**: Hypothetical probability of chance agreement.

**Codex Implementation Instructions:**
- Use `sklearn.metrics.cohen_kappa_score`.
- Treat the 8 primary categories as nominal classes.
- Calculate an overall $\kappa$, and then calculate independent $\kappa$ scores stratified by document complexity (Medium, High, Very High).
- **Threshold**: Throw an assertion error if $\kappa < 0.85$.

## 2. Entity Span Extraction: Macro & Micro F1 Score
For bounding box extractions, agreement is measured at the token/span level. 

**Mathematical Definition:**
We define a True Positive (TP) when both Annotator A and Annotator B extract the same entity type with a valid span overlap.
- **Strict Match**: Exact match on start index, end index, and entity type.
- **Relaxed Match**: Jaccard similarity of bounding boxes/character spans $\ge 0.50$.

**Formulas:**
- $\text{Precision} = \frac{TP}{TP + FP}$
- $\text{Recall} = \frac{TP}{TP + FN}$
- $\text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$

**Codex Implementation Instructions:**
- Implement a bipartite matching algorithm to pair spans between Annotator A and Annotator B to maximize global overlap.
- Calculate **Macro F1** (unweighted average of F1 scores across all 22 entity types) to ensure rare entities are weighted equally.
- Calculate **Micro F1** (global aggregate of all TPs, FPs, FNs) to reflect overall extraction quality.
- **Threshold**: Throw an assertion error if Entity-Level Macro F1 $< 0.85$.

## 3. Statistical Significance
**Codex Implementation Instructions:**
- Implement a Bootstrapping routine (N=1000 resamples with replacement).
- Compute the 95% Confidence Interval for both Cohen's Kappa and Macro F1.
- Output the final results to `reports/iaa_report_final.json` in a structured format.
