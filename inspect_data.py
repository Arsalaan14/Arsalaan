import json

with open("d:/Code_wid_pablo/CTS-Hackathon/data/patient_records_50.json", "r") as f:
    data = json.load(f)

for p in data["patients"]:
    for visit in p.get("visits", []):
        keys = list(visit.keys())
        if any(k not in ["date", "doctor", "reason"] for k in keys):
            print(f"Patient {p['patient_id']} visit keys: {keys}")
    for med in p.get("medications", []):
        keys = list(med.keys())
        if any(k not in ["name", "dosage", "frequency"] for k in keys):
            print(f"Patient {p['patient_id']} medication keys: {keys}")
    for lab in p.get("lab_reports", []):
        keys = list(lab.keys())
        if any(k not in ["test_name", "value", "date"] for k in keys):
            print(f"Patient {p['patient_id']} lab report keys: {keys}")
