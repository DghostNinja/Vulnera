import os
import glob
import requests

def run_wapiti(target_url):
    # Run Wapiti scan
    os.system(f"wapiti -u {target_url} -o report.html")

    # Find the actual report file inside the 'report.html/' directory
    report_files = glob.glob("report.html/*.html")  # List all HTML reports
    if not report_files:
        raise FileNotFoundError("No report file found in report.html/")

    latest_report = max(report_files, key=os.path.getctime)  # Get the newest report file

    # Read the latest Wapiti report
    with open(latest_report, "r") as f:
        return f.read()

def send_to_telegram(message, chat_id, token):
    # Send message to Telegram
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    target_url = "http://testphp.vulnweb.com"  # Replace with your target URL
    telegram_token = "YOUR_TELEGRAM_BOT_TOKEN"
    telegram_chat_id = "YOUR_TELEGRAM_CHAT_ID"

    try:
        # Run Wapiti scan and get the report content
        report = run_wapiti(target_url)

        # Send report to Telegram
        send_to_telegram(f"Wapiti Scan Report:\n{report[:4000]}", telegram_chat_id, telegram_token)  # Telegram limit is 4096 chars

    except Exception as e:
        print(f"Error: {e}")
