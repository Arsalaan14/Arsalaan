import os
import sys
import json
import unittest

# Add root folder to sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import config
from vector_embedding.normalization import normalize_single_patient
from retrieval.query_processor import process_query
from retrieval.retriever import PatientRetriever
from backend.auth import redact_patient_data, AUDIT_LOG_PATH, PERSONAS, get_auth_context, audit_log_action

def normalize_raw_patient_data(raw_data):
    patients = raw_data.get("patients", [])
    normalized = []
    encounters = []
    notes = []
    for i, p in enumerate(patients):
        norm = normalize_single_patient(p, i)
        normalized.append(norm["patient"])
        encounters.extend(norm["encounters"])
        notes.extend(norm["notes"])
    return {
        "patients": normalized,
        "encounters": encounters,
        "notes": notes
    }

class TestMedicalSecurityAndRAG(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Read a subset of raw patients data for quick tests
        with open(config.JSON_DATA_PATH, "r", encoding="utf-8") as f:
            cls.raw_data = json.load(f)
        cls.normalized_data = normalize_raw_patient_data(cls.raw_data)

    def test_canonical_normalization(self):
        """Verify the raw nested JSON parses into normalized entity types with provenance tags."""
        self.assertIn("patients", self.normalized_data)
        self.assertIn("encounters", self.normalized_data)
        self.assertIn("notes", self.normalized_data)
        
        # Verify the structure has clinical and provider entities
        p_entities = self.normalized_data["patients"]
        self.assertGreater(len(p_entities), 0)
        
        # Check that provenance paths start with patients[x]
        first_patient = p_entities[0]
        self.assertIn("patient_id", first_patient)
        pid_field = first_patient.get("patient_id", {})
        self.assertTrue(pid_field.get("source_path", "").startswith("patients[0]"))

    def test_query_understanding_filters(self):
        """Verify query parsing extracts metadata filters and keywords from natural language sentences."""
        q1 = "Show me lab tests for patient P009 and check they have cardiac values"
        parsed1 = process_query(q1)
        self.assertIn("P009", parsed1)
        self.assertIn("lab", parsed1.lower())
        
        q2 = "Medications of P003 and allergic items"
        parsed2 = process_query(q2)
        self.assertIn("P003", parsed2)
        self.assertIn("medication", parsed2.lower())

    def test_insurer_data_redaction(self):
        """Validate that contact details and name fields are masked for Insurer role."""
        raw_p = {
            "patient_id": "P001",
            "name": "John Doe",
            "age": 45,
            "contact": {
                "phone": "+1-555-0199",
                "email": "johndoe@example.com"
            },
            "address": "123 Elm Street, Cityville"
        }
        
        # Provider sees full data
        provider_data = redact_patient_data(raw_p, "provider")
        self.assertEqual(provider_data["name"], "John Doe")
        self.assertEqual(provider_data["contact"]["phone"], "+1-555-0199")
        
        # Insurer triggers masking
        insurer_data = redact_patient_data(raw_p, "insurer")
        self.assertEqual(insurer_data["name"], "Patient P001")
        self.assertEqual(insurer_data["contact"]["phone"], "[REDACTED FOR INSURER]")
        self.assertEqual(insurer_data["contact"]["email"], "[REDACTED FOR INSURER]")
        self.assertEqual(insurer_data["address"], "[REDACTED FOR INSURER]")

    def test_patient_boundary_access(self):
        """Validate database retrieval boundaries for patients to prevent cross-viewing records."""
        # Initialize helper retriever
        retriever = PatientRetriever()
        
        # Patient P009 queries - should succeed but filter scope
        docs_p009 = retriever.retrieve_documents("medications", role="patient", auth_patient_id="P009")
        metadatas = docs_p009.get("metadatas", [[]])[0]
        for meta in metadatas:
            self.assertEqual(meta.get("patient_id"), "P009")
            
        # P002 query filters should restrict only to P002
        docs_p002 = retriever.retrieve_documents("blood report for P009", role="patient", auth_patient_id="P002")
        metadatas_p002 = docs_p002.get("metadatas", [[]])[0]
        for meta in metadatas_p002:
            self.assertEqual(meta.get("patient_id"), "P002")

    def test_header_auth_helpers(self):
        """Verify headers parse role identity and active boundaries correctly."""
        headers = {
            "Authorization": "Bearer MockToken-patient-P005",
            "X-User-Role": "admin" # Auth headers should take precedence over X-Headers
        }
        name, role, auth_pid = get_auth_context(headers)
        self.assertEqual(role, "patient")
        self.assertEqual(auth_pid, "P005")
        self.assertEqual(name, "Patient P005")

        headers_no_token = {
            "X-User-Role": "insurer"
        }
        name, role, auth_pid = get_auth_context(headers_no_token)
        self.assertEqual(role, "insurer")
        self.assertIsNone(auth_pid)

    def test_audit_logs_record(self):
        """Check that the audit log file database records entries and exists."""
        audit_log_action("TestUser", "admin", "TEST_SETUP", "Initializing test baseline logs")
        self.assertTrue(os.path.exists(AUDIT_LOG_PATH))
        with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
            logs = json.loads(f.read())
        self.assertGreater(len(logs), 0)
        
        # First check that schema entries match logging specification
        latest_entry = logs[-1]
        self.assertIn("timestamp", latest_entry)
        self.assertIn("user", latest_entry)
        self.assertIn("role", latest_entry)
        self.assertIn("action", latest_entry)
        self.assertIn("status", latest_entry)

if __name__ == "__main__":
    unittest.main()
