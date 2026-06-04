# Quality Assurance Workflow Specification

## 1. Five-Stage QA Pipeline

| Stage | Actor | Input | Output | Quality Gate |
|---|---|---|---|---|
| 1. Pre-Screening | QA Lead | Raw document | Screened document | Legibility >= 60% |
| 2. Primary Annotation | Annotator | Screened document | First-pass annotations | Schema validation passes |
| 3. Self-Review | Same Annotator | First-pass annotations | Reviewed annotations | Zero schema errors |
| 4. Peer Review | Reviewer | Reviewed annotations | Adjudicated annotations | Agreement >= 90% |
| 5. Final QA | QA Lead | Adjudicated annotations | Gold-standard annotations | 10% sample achieves 98%+ |

## 2. Roles
- **Annotator**: Primary labeling.
- **Reviewer**: Peer checking 30% to 50% depending on phase.
- **Adjudicator**: Resolves disagreements.
- **QA Lead**: Manages pipeline, configures Label Studio.

## 3. Escalation Matrix
| Issue Type | Severity | Escalation Path | Resolution SLA |
|---|---|---|---|
| Schema doesn't accommodate entity | High | Annotator > QA Lead > Schema Designer | 4 hours |
| Guideline ambiguity | Medium | Annotator > Reviewer > Guideline Author | 8 hours |
| Inter-annotator disagreement | Medium | Annotator > Peer > Adjudicator | 12 hours |
| Document quality below threshold | Low | Annotator > QA Lead | 24 hours |
| Systematic annotation error | Critical | QA Lead > Re-annotate | 48 hours |

## 4. Sampling Strategy
- First 30 documents: 100% full review
- Documents 31-80: 50% random sample
- Documents 81-140: 30% random sample
- Documents 141-200: 20% random + 100% flagged
- Final QA pass: 10% stratified random sample
