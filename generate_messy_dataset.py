import json
import random
import uuid
from datetime import datetime, timedelta

def get_messy_key(base_key):
    variations = {
        "patient_id": ["patient_id", "pat_id", "pid", "id", "patientId"],
        "name": ["name", "patient_name", "full_name", "nm"],
        "age": ["age", "patient_age", "years", "ag"],
        "gender": ["gender", "sex", "patient_gender", "gen"],
        "blood_group": ["blood_group", "blood_type", "bg", "b_group"],
        "address": ["address", "addr", "location", "residence"],
        "contact": ["contact", "contact_info", "comm", "phone_and_email"],
        
        "allergies": ["allergies", "allergy", "allergies_list", "alrg", "all"],
        "careplans": ["careplans", "care_plan", "cplan", "plans", "cp"],
        "claims": ["claims", "claim_info", "clms", "insurance_claims"],
        "claims_transactions": ["claims_transactions", "transactions", "claim_tx", "ctx"],
        "conditions": ["conditions", "condition", "cond", "con", "dx"],
        "devices": ["devices", "device", "dev", "equipment"],
        "encounters": ["encounters", "encounter", "visits", "visit_history", "enc"],
        "imaging_studies": ["imaging_studies", "imaging", "scans", "img_std", "radiology"],
        "immunizations": ["immunizations", "immunization", "vaccines", "imm", "vax"],
        "medications": ["medications", "medication", "meds", "rx", "drugs"],
        "observations": ["observations", "observation", "obs", "vitals", "measurements"],
        "organizations": ["organizations", "org", "hospital_org", "facility"],
        "payer_transitions": ["payer_transitions", "insurance_transitions", "pyr_tx"],
        "payers": ["payers", "insurance", "payer_info", "health_plan"],
        "procedures": ["procedures", "procedure", "surgery", "proc", "surg"],
        "providers": ["providers", "provider", "doctors", "prov", "clinician"],
        "supplies": ["supplies", "supply", "medical_supplies", "spl"]
    }
    
    if base_key in variations:
        return random.choice(variations[base_key])
    return base_key

def random_date(start_year=2010, end_year=2023):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

def generate_messy_patient(pid_num):
    patient = {}
    
    # Basic Info
    patient[get_messy_key("patient_id")] = f"PID{pid_num:05d}"
    patient[get_messy_key("name")] = random.choice(["John Doe", "Jane Wilson", "Victor Smith", "Peggy Brown", "Alice Johnson", "Bob Miller"])
    patient[get_messy_key("age")] = random.randint(1, 100)
    patient[get_messy_key("gender")] = random.choice(["Male", "Female", "Other"])
    patient[get_messy_key("blood_group")] = random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    patient[get_messy_key("address")] = f"{random.randint(100, 9999)} {random.choice(['Maple', 'Cedar', 'Oak', 'Pine'])} St, City"
    
    patient[get_messy_key("contact")] = {
        random.choice(["phone", "ph", "tel", "telephone"]): f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        random.choice(["email", "mail", "email_address"]): f"user{pid_num}@example.com"
    }

    # Complex / Messy nesting structures for the medical data
    
    # 1. Allergies: list of dicts, or strings, or dict with nested meds/conds
    allergy_key = get_messy_key("allergies")
    if random.choice([True, False]):
        # Simple list of strings
        patient[allergy_key] = [random.choice(["Peanuts", "Penicillin", "Latex", "Pollen"])]
    else:
        # Complex nesting
        patient[allergy_key] = []
        for _ in range(random.randint(1, 3)):
            al = {
                random.choice(["allergen", "name", "substance"]): random.choice(["Peanuts", "Penicillin", "Latex", "Pollen"]),
                random.choice(["severity", "level"]): random.choice(["Mild", "Moderate", "Severe"]),
            }
            if random.random() > 0.5:
                # Nest medication inside allergy
                al[get_messy_key("medications")] = {
                    "prescribed": random.choice(["Epinephrine", "Antihistamine"]),
                    get_messy_key("conditions"): random.choice(["Anaphylaxis", "Rash"])
                }
            patient[allergy_key].append(al)

    # 2. Conditions
    patient[get_messy_key("conditions")] = [random.choice(["Hypertension", "Diabetes", "Asthma", "Osteoarthritis"]) for _ in range(random.randint(1, 3))]

    # 3. Medications
    meds = []
    for _ in range(random.randint(1, 4)):
        med = {
            random.choice(["name", "drug"]): random.choice(["Lisinopril", "Amlodipine", "Omeprazole", "Gabapentin", "Atorvastatin"]),
            random.choice(["dosage", "dose"]): f"{random.choice([100, 200, 500])}mg",
        }
        if random.random() > 0.5:
            # nest condition inside medication
            med[get_messy_key("conditions")] = random.choice(["Hypertension", "Pain", "Cholesterol"])
        meds.append(med)
    patient[get_messy_key("medications")] = meds

    # 4. Encounters
    encounters = []
    for _ in range(random.randint(1, 3)):
        encounters.append({
            random.choice(["date", "dt"]): random_date(),
            random.choice(["doctor", "doc", "physician"]): f"Dr. {random.choice(['Adams', 'Davis', 'Baker', 'Smith'])}",
            random.choice(["reason", "chief_complaint"]): random.choice(["Headache", "Routine checkup", "Follow-up", "Back pain"])
        })
    patient[get_messy_key("encounters")] = encounters

    # 5. Observations
    obs = []
    for _ in range(random.randint(1, 3)):
        obs.append({
            random.choice(["type", "name", "test"]): random.choice(["Blood Pressure", "Heart Rate", "Weight"]),
            random.choice(["value", "val"]): str(random.randint(60, 200))
        })
    patient[get_messy_key("observations")] = obs

    # 6. Procedures
    patient[get_messy_key("procedures")] = [{
        "name": random.choice(["Appendectomy", "Knee Replacement", "Cataract Surgery", "Biopsy"]),
        "date": random_date()
    } for _ in range(random.randint(0, 2))]

    # 7. Immunizations
    patient[get_messy_key("immunizations")] = [random.choice(["Flu Vaccine", "COVID-19", "Tetanus"]) for _ in range(random.randint(0, 3))]

    # 8. Imaging Studies
    patient[get_messy_key("imaging_studies")] = [{
        "modality": random.choice(["X-Ray", "MRI", "CT Scan"]),
        "body_site": random.choice(["Chest", "Knee", "Brain"])
    } for _ in range(random.randint(0, 2))]

    # 9. Claims and Transactions (Nested deeply)
    claims = []
    for _ in range(random.randint(1, 2)):
        claim = {
            "claim_id": str(uuid.uuid4())[:8],
            "total_cost": round(random.uniform(100.0, 5000.0), 2),
            get_messy_key("claims_transactions"): [
                {
                    "amount": round(random.uniform(10.0, 500.0), 2),
                    "status": random.choice(["Paid", "Pending", "Denied"])
                }
            ]
        }
        claims.append(claim)
    patient[get_messy_key("claims")] = claims

    # 10. Payers & Transitions
    patient[get_messy_key("payers")] = {
        "primary": random.choice(["Medicare", "Blue Cross", "Aetna", "Cigna"]),
        get_messy_key("payer_transitions"): [
            {"from": "None", "to": "Medicare", "date": random_date()}
        ]
    }

    # 11. Providers & Organizations
    patient[get_messy_key("providers")] = [
        {
            "name": f"Dr. {random.choice(['Adams', 'Davis', 'Baker', 'Smith'])}",
            "specialty": random.choice(["Cardiology", "General Practice", "Orthopedics"]),
            get_messy_key("organizations"): {
                "name": random.choice(["Springfield Hospital", "General Clinic", "City Medical Center"])
            }
        }
    ]

    # 12. Careplans
    patient[get_messy_key("careplans")] = [{
        "title": random.choice(["Diabetes Management", "Weight Loss", "Post-op recovery"]),
        "status": random.choice(["Active", "Completed"])
    } for _ in range(random.randint(0, 2))]

    # 13. Devices
    patient[get_messy_key("devices")] = [random.choice(["Pacemaker", "Insulin Pump", "Hearing Aid"]) for _ in range(random.randint(0, 1))]
    
    # 14. Supplies
    patient[get_messy_key("supplies")] = [random.choice(["Bandages", "Syringes", "Gauze"]) for _ in range(random.randint(0, 2))]
    
    return patient

if __name__ == "__main__":
    patients = [generate_messy_patient(i) for i in range(1, 101)]
    output_data = {"patients": patients}
    
    with open("c:/Users/navee/Desktop/mock_hack/CTS-Hackathon/data/patient_records_messy.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    print("Generated 100 messy patient records successfully!")
