import os
import requests
import subprocess
import json

# Load secrets from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def run_wapiti(target_url):
    """Run Wapiti scan and return results."""
    output_file = "report.json"
    
    # Run Wapiti scan in JSON format
    cmd = ["wapiti", "-u", target_url, "-f", "json", "-o", output_file]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Read JSON report
    with open(output_file, "r") as f:
        return json.load(f)

def send_to_telegram(message):
    """Send message to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    target_url = "http://testphp.vulnweb.com"  # Replace with your target

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: TELEGRAM_TOKEN or TELEGRAM_CHAT_ID is not set.")
        exit(1)

    report = run_wapiti(target_url)

    # Extract and format important info
    vulnerabilities = report.get("vulnerabilities", [])
    message = f"Wapiti Scan Report for {target_url}\n\n"

    for vuln in vulnerabilities:
        message += f"- {vuln['name']}: {vuln['description']}\n"

    # Send report summary
    send_to_telegram(message[:4096])  # Telegram message limit
