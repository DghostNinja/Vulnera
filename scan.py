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
    return latest_report  # Return the path to the report file

def send_to_telegram(file_path, chat_id, token):
    # Send report as a file
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    
    with open(file_path, "rb") as file:
        files = {"document": file}
        payload = {"chat_id": chat_id, "caption": "Wapiti Scan Report"}
        response = requests.post(url, data=payload, files=files)
    
    return response.json()

if __name__ == "__main__":
    target_url = "http://testphp.vulnweb.com"  # Replace with your target URL
    telegram_token = os.getenv("TELEGRAM_TOKEN")  # Get token from env
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")  # Get chat ID from env

    try:
        # Run Wapiti scan and get the report file path
        report_file = run_wapiti(target_url)

        # Send the report as a file to Telegram
        response = send_to_telegram(report_file, telegram_chat_id, telegram_token)
        print(response)  # Debugging

    except Exception as e:
        print(f"Error: {e}")
