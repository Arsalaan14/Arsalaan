import sys
import json
import traceback

sys.path.append("c:/Users/navee/Desktop/mock_hack/CTS-Hackathon/vector_embedding")
import normalization

def main():
    input_file = "c:/Users/navee/Desktop/mock_hack/CTS-Hackathon/data/patient_records_messy.json"
    output_file = "c:/Users/navee/Desktop/mock_hack/CTS-Hackathon/data/patient_records_normalized_test.json"
    
    try:
        print("Starting normalization...")
        normalized = normalization.normalize_dataset(input_file, output_file)
        print(f"Successfully normalized {len(normalized)} patients.")
        
        # Spot check first patient
        p = normalized[0]
        print(f"\nSample Patient ID: {p['patient'].get('patient_id', {}).get('value')}")
        print(f"Total Conditions found: {len(p['conditions'])}")
        print(f"Total Medications found: {len(p['medications'])}")
        print(f"Total Encounters found: {len(p['encounters'])}")
        print(f"Total Allergies found: {len(p['allergies'])}")
        print(f"Total Payer records found: {len(p['payers'])}")
        
        # Make sure that complex structures were mapped to the standard
        print(f"\nRaw keys in medication 0 (if exists): {p['medications'][0].keys() if p['medications'] else 'None'}")
        
    except Exception as e:
        print(f"Error during normalization: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
