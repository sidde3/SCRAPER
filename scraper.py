import random
import string
import logging
import json
import re
from playwright.sync_api import sync_playwright
from tenacity import retry, stop_after_attempt, wait_exponential

# Proxy list
proxies = [
    {'http': 'http://localhost:9090'},
    {'http': 'http://localhost:9091'}
]

# Sample insurers
insurers = ["MockInsureX", "DentalSecure", "HealthLine", "SmileCover", "BrightDental"]

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_random_proxy():
    return random.choice(proxies)

def generate_random_patient_id(length=6):
    """Generate a random alphanumeric patient ID like A9Z5B3"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_random_insurer():
    return random.choice(insurers)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def scrape_eligibility(patient_id, insurer_name):
    proxy = get_random_proxy()
    browser = None

    url = f"http://localhost:8080/eligibility/{patient_id}/"
    logging.info(f"Scraping URL: {url}")

    with sync_playwright() as p:
        try:
            # Launch browser with or without proxy
            if proxy:
                browser = p.chromium.launch(proxy={"server": proxy['http']}, headless=True)
            else:
                browser = p.chromium.launch(headless=True)

            page = browser.new_page()
            page.goto(url, timeout=10000)
            page.wait_for_load_state('networkidle')

            # Extract full text from page
            page_text = page.inner_text("body")

            # Extract eligibility status from text
            match = re.search(r"Eligibility Status:\s*(\w+)", page_text)
            if not match:
                raise ValueError("Eligibility status not found in page")

            status = match.group(1).strip().lower()

            return {
                "patient_id": patient_id,
                "eligibility_status": status,
                "insurer_name": insurer_name
            }

        except Exception as e:
            logging.error(f"[ScraperError] Patient ID: {patient_id} | Error: {str(e)}")
            raise
        finally:
            if browser:
                browser.close()

# Main program
if __name__ == "__main__":
    patient_id = generate_random_patient_id()
    insurer_name = get_random_insurer()
    try:
        result = scrape_eligibility(patient_id, insurer_name)
        print(json.dumps(result, indent=2))
    except Exception as e:
        logging.error(f"[FinalError] Scraper failed after retries | {str(e)}")
