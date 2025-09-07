import os
import requests
import logging
import json
import random
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/eligibility_agent_post.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Simulated list of insurers
insurers = ["MockInsureX", "DentalSecure", "BrightDental", "CarePlus", "ToothSure"]

def get_random_insurer():
    return random.choice(insurers)

def generate_patient_id():
    return "D" + ''.join(random.choices("0123456789", k=5))

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
def check_eligibility_api(patient_id, url, credentials):
    payload = {
        "username": credentials["username"],
        "password": credentials["password"],
        "patient_id": patient_id
    }
    
    logging.info(f"Calling API for patient {patient_id} at {url}")

    response = requests.post(url, data=payload, timeout=5)

    if response.status_code != 200:
        raise Exception(f"Bad response: {response.status_code}")
    
    data = response.json()

    if "eligibility_status" not in data:
        raise ValueError("Missing eligibility_status in response")

    return {
        "patient_id": patient_id,
        "eligibility_status": data["eligibility_status"].lower(),
        "insurer_name": get_random_insurer(),
        "timestamp": datetime.utcnow().isoformat()
    }

def fallback_response(patient_id):
    logging.warning(f"Fallback triggered for patient {patient_id}")
    return {
        "patient_id": patient_id,
        "eligibility_status": "unknown",
        "insurer_name": "ManualFallback",
        "timestamp": datetime.utcnow().isoformat()
    }

def run_verification(input_data):
    try:
        return check_eligibility_api(
            input_data["patient_id"],
            input_data["insurer_portal_url"],
            input_data["credentials"]
        )
    except Exception as e:
        logging.error(f"Verification failed for {input_data['patient_id']}: {e}")
        return fallback_response(input_data["patient_id"])

if __name__ == "__main__":
    # Run 5 test cases
    for _ in range(5):
        patient_id = generate_patient_id()
        input_record = {
            "patient_id": patient_id,
            "insurer_portal_url": "http://localhost:8080/eligibility/check-eligibility/",
            "credentials": {"username": "admin", "password": "admin"}
        }

        result = run_verification(input_record)
        print(json.dumps(result, indent=2))
