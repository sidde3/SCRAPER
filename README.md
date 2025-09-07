# 🦷 Dental Insurance Eligibility Verification Agent (PoC)

This Proof of Concept (PoC) demonstrates a basic eligibility verification system for dental insurance. It includes two main components:

- `scraper.py`: A web scraper using Playwright to simulate scraping a mock insurer portal.
- `ai_agent.py`: An intelligent agent that uses an API to verify eligibility and falls back to a default response if the API fails.

## 📁 Project Structure

```text
├── scraper.py                  # Web scraper with proxy rotation & retry logic
├── ai_agent.py                 # API-based eligibility checker with fallback
├── logs/                       # Logs written here
└── mock_insurer_django/        # Django-based mock insurance portal
```

## 🧩 Components

### ✅ `scraper.py`

- Scrapes mock eligibility data from:
  `http://localhost:8080/eligibility/<patient_id>/`
- Uses rotating proxies (via `mitmdump`) on ports `9090` and `9091`.
- Includes:

  - Retry with exponential backoff (via `tenacity`)
  - Proxy support
  - Logging
  - Regex parsing for `Eligibility Status`
  - Outputs normalized JSON with fields:

    ```json
    {
      "patient_id": "D12345",
      "eligibility_status": "eligible",
      "insurer_name": "MockInsureX"
    }
    ```

**Proxy Setup (for testing):**
Run proxies in separate terminals:

```bash
mitmdump -p 9090
mitmdump -p 9091
```

### 🤖 `ai_agent.py`

- Sends a `POST` request to the Django app at:

  ```bash
  http://localhost:8080/eligibility/check-eligibility/
  ```

- Payload:

  ```json
  {
    "username": "admin",
    "password": "admin",
    "patient_id": "D12365"
  }
  ```

- If the request fails, falls back to a manual response with `"unknown"` status.
- Logs activity in `logs/eligibility_agent_post.log`.
- Outputs structured JSON with a timestamp:

  ```json
  {
    "patient_id": "D12365",
    "eligibility_status": "eligible",
    "insurer_name": "DentalSecure",
    "timestamp": "2025-09-07T14:32:00.123Z"
  }
  ```

## ⚙️ Prerequisites

Install required Python packages:

```bash
pip install playwright tenacity requests
playwright install
```

Ensure browsers are installed after installing Playwright:

```bash
playwright install
```

## 🧪 Running the Mock Insurance Portal

This project assumes a Django-based portal is running locally on port `8080`.

### Start the server:

```bash
python manage.py runserver 8080
```

### Create a superuser (if needed):

```bash
python manage.py createsuperuser
```

## 🚀 How to Run

### Scraper:

```bash
python scraper.py
```

### AI Agent:

```bash
python ai_agent.py
```

AI Agent runs 5 test cases and logs fallback behavior if scraper/API fails.

## 📝 Logs

- Scraper logs to **console**
- AI Agent logs to:
  `logs/eligibility_agent_post.log`

## 📦 Sample Output

```json
{
  "patient_id": "D12365",
  "eligibility_status": "eligible",
  "insurer_name": "CarePlus",
  "timestamp": "2025-09-07T13:20:15.921Z"
}
```

## ✅ Features

- Proxy rotation (bonus requirement)
- Retry + exponential backoff
- Scraper error classification and fallback
- Alphanumeric Patient IDs and randomized insurers
- Output in normalized, structured JSON
