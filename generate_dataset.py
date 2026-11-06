import json
import random
from datetime import datetime, timedelta

def get_random_date(start_year=2020, end_year=2023):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Mallory", "Victor", "Peggy", "Sybil", "Trent", "Walter"]
last_names = ["Smith", "Doe", "Johnson", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin"]
genders = ["Male", "Female", "Other"]
blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
med_names = ["Lisinopril", "Metformin", "Atorvastatin", "Amlodipine", "Omeprazole", "Losartan", "Albuterol", "Gabapentin", "Hydrochlorothiazide", "Sertraline"]
dosages = ["10mg", "20mg", "50mg", "100mg", "200mg", "500mg"]
frequencies = ["Once daily", "Twice daily", "Every 8 hours", "As needed"]
doctors = ["Dr. Smith", "Dr. Adams", "Dr. Baker", "Dr. Clark", "Dr. Davis", "Dr. Evans", "Dr. Frank", "Dr. Ghosh"]
reasons = ["Routine checkup", "Fever and cough", "Back pain", "Headache", "Follow-up", "Blood pressure management", "Diabetes screening", "Annual physical"]
test_names = ["CBC", "Lipid Panel", "HbA1c", "Thyroid Panel", "Vitamin D", "Comprehensive Metabolic Panel", "Urinalysis"]
allergies_list = ["Penicillin", "Peanuts", "Dust mites", "Latex", "Pollen", "Sulfa drugs", "Aspirin", "Dairy"]
conditions_list = ["Hypertension", "Type 2 Diabetes", "Asthma", "Hyperlipidemia", "Hypothyroidism", "Migraine", "Osteoarthritis", "Anxiety", "Depression"]

def generate_patient(pid_num):
    pid = f"PID{pid_num:05d}"
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    age = random.randint(18, 90)
    gender = random.choice(genders)
    blood_group = random.choice(blood_groups)
    
    patient = {
        "patient_id": pid,
        "name": name,
        "age": age,
        "gender": gender,
        "blood_group": blood_group,
        "address": f"{random.randint(100, 9999)} {random.choice(['Main St', 'Oak Ave', 'Pine Ln', 'Maple Dr', 'Cedar Ct'])}, {random.choice(['Springfield', 'Riverside', 'Centerville', 'Georgetown'])}",
        "contact": {
            "phone": f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "email": f"{name.split()[0].lower()}.{name.split()[1].lower()}@example.com"
        }
    }
    
    # Randomly nesting arrays
    # Medications
    if random.random() > 0.2:
        num_meds = random.randint(1, 4)
        meds = []
        for _ in range(num_meds):
            meds.append({
                "name": random.choice(med_names),
                "dosage": random.choice(dosages),
                "frequency": random.choice(frequencies),
                "start_date": get_random_date(2018, 2023)
            })
        patient["medications"] = meds
        
    # Visits
    if random.random() > 0.1:
        num_visits = random.randint(1, 5)
        visits = []
        for _ in range(num_visits):
            visits.append({
                "date": get_random_date(2022, 2023),
                "doctor": random.choice(doctors),
                "reason": random.choice(reasons)
            })
        patient["visits"] = visits
        
    # Lab Reports
    if random.random() > 0.3:
        num_labs = random.randint(1, 3)
        labs = []
        for _ in range(num_labs):
            test = random.choice(test_names)
            value = str(random.randint(10, 200)) if test != "HbA1c" else f"{random.uniform(4.0, 10.0):.1f}"
            labs.append({
                "test_name": test,
                "value": value,
                "date": get_random_date(2023, 2023)
            })
        patient["lab_reports"] = labs
        
    # Allergies (mixed nesting - some string, some dict as per normalizer logic)
    if random.random() > 0.4:
        num_allergies = random.randint(1, 3)
        allergies = []
        for _ in range(num_allergies):
            alg = random.choice(allergies_list)
            if random.random() > 0.5:
                allergies.append(alg) # string
            else:
                allergies.append({"allergen": alg, "severity": random.choice(["Mild", "Moderate", "Severe"])}) # dict
        patient["allergies"] = allergies
        
    # Conditions
    if random.random() > 0.2:
        num_conds = random.randint(1, 4)
        conds = random.sample(conditions_list, num_conds)
        patient["conditions"] = conds

    return patient

if __name__ == "__main__":
    num_records = 75
    patients = [generate_patient(i) for i in range(1, num_records + 1)]
    dataset = {"patients": patients}
    
    with open("data/patient_records_random.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    print(f"Generated {num_records} patient records in data/patient_records_random.json")
