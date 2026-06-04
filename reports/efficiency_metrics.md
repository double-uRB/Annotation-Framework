# Annotation Efficiency Metrics

1. **Time per Document**:
   - Total annotation time including entity extraction and review.
   - Granularity: Per document.
   - Outcome: Mean, median, P90, P95 by category.

2. **Entities per Hour**:
   - Number of entities annotated per hour of work.
   - Granularity: Per session.
   - Outcome: Show learning curve.

3. **Error Rate Over Time**:
   - Proportion of annotations corrected during review.
   - Granularity: Per day.
   - Outcome: Decrease from Day 1 to Day 7.

4. **Annotation Throughput**:
   - Documents fully annotated per hour.
   - Granularity: Per day.
   - Outcome: Throughput by complexity tier.

5. **Review Time Ratio**:
   - Time spent on review vs. initial annotation.
   - Granularity: Per day.
   - Outcome: Typically 0.3-0.5x of annotation time.

## 7. Time-Tracking Strategy & Expected Baselines
To accurately measure efficiency, the following baseline annotation times are defined per document complexity tier:
- **Low-Medium Complexity** (Payment Receipts, Bank Statements): 1.5 - 2.5 minutes per document.
- **High Complexity** (Insurance Policies, Income Tax Returns): 4.0 - 6.5 minutes per document.
- **Very High Complexity** (Loan Agreements, Financial Statements, Regulatory Filings): 8.0 - 14.0 minutes per document.

*Tracking Implementation:* Annotators will use a timer integrated into Label Studio. The clock stops automatically during adjudication or idle states. The system will record `time_to_annotate_seconds` in the `quality_metadata` node of the JSONL schema.

## 8. Return on Investment (ROI) of Pre-Annotation Models
Once the dataset reaches 100 documents, a preliminary zero-shot or few-shot extraction model will be deployed to pre-annotate incoming documents.

**ROI Calculation Model:**
- **Manual Cost Baseline ($C_m$):** Average hourly rate of annotator $\times$ Total manual time required.
- **Pre-Annotation Cost ($C_p$):** Model inference cost + Reviewer hourly rate $\times$ Total review time required.
- **Time Savings ($T_{\Delta}$):** $T_{manual} - T_{review}$

**Expected Target:**
Pre-annotation must reduce total human-in-the-loop time by at least **40%** ($T_{review} \le 0.60 \times T_{manual}$) without dropping IAA scores below the 0.85 threshold. ROI is validated when $C_p < C_m$ and velocity scales linearly.
