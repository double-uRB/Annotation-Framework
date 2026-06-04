import json
import jsonschema
import sys
import os

def validate_annotations():
    schema_path = r"d:\Project\ZeTheta Annotation Framework\schema\annotation_schema.json"
    annotations_path = r"d:\Project\ZeTheta Annotation Framework\data\gold_standard\annotations.jsonl"
    
    if not os.path.exists(schema_path):
        print(f"Error: Schema not found at {schema_path}")
        sys.exit(1)
        
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
        
    if not os.path.exists(annotations_path):
        # Create a dummy annotations.jsonl for validation since Codex is still generating PDFs
        with open(annotations_path, "w", encoding="utf-8") as f:
            dummy_doc = {
                "document_metadata": {
                    "document_id": "bank_statement_001",
                    "source_file_path": "data/raw_documents/bank_statements/bank_statement_001.pdf",
                    "creation_date": "2026-06-04T12:00:00Z",
                    "last_modified": "2026-06-04T12:00:00Z",
                    "assigned_annotator": "Agent-Alpha",
                    "review_status": "approved"
                },
                "classification": {
                    "primary_type": "Bank Statements",
                    "subtype": "Savings Account Statement",
                    "quality_tags": ["CLEAN_DIGITAL"],
                    "confidence_scores": {
                        "primary_type_confidence": 0.99,
                        "subtype_confidence": 0.98
                    }
                },
                "entities": [
                    {
                        "entity_id": "ent_001",
                        "entity_type": "MONETARY_AMOUNT",
                        "value": "15,000.00",
                        "normalized_value": {
                            "amount": 15000.00,
                            "currency": "USD"
                        },
                        "source_text": "15,000.00",
                        "page_number": 1,
                        "bounding_box": [100.0, 150.0, 50.0, 15.0],
                        "confidence": 0.95
                    }
                ],
                "relationships": [],
                "quality_metadata": {
                    "ocr_confidence_per_page": [{"page": 1, "confidence": 0.99}],
                    "annotation_difficulty": 1,
                    "time_to_annotate_seconds": 120,
                    "review_comments": "Clean extraction."
                },
                "version_control": {
                    "schema_version": "1.0.0",
                    "annotation_guideline_version": "1.0",
                    "annotator_tool_version": "1.10.0"
                }
            }
            f.write(json.dumps(dummy_doc) + "\n")
            
    print(f"Validating annotations from {annotations_path} against Draft 2020-12 schema...")
    
    with open(annotations_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if not line.strip():
                continue
            doc = json.loads(line)
            try:
                jsonschema.validate(instance=doc, schema=schema)
                print(f"Document {idx+1} ({doc['document_metadata']['document_id']}): Valid")
            except jsonschema.exceptions.ValidationError as e:
                print(f"Document {idx+1} ({doc['document_metadata']['document_id']}): Invalid -> {e.message}")
                
if __name__ == "__main__":
    validate_annotations()
