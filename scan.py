import os
import glob
import requests

def run_wapiti(target_url):
    """Runs Wapiti scan on the target URL and returns the report file path."""
    os.system(f"wapiti -u {target_url} -o report.html")

    # Find the actual report file inside the 'report.html/' directory
    report_files = glob.glob("report.html/*.html")  # List all HTML reports
    if not report_files:
        raise FileNotFoundError("No report file found in report.html/")

    latest_report = max(report_files, key=os.path.getctime)  # Get the newest report file
    return latest_report  # Return the path to the report file

def send_to_telegram(file_path, chat_id, token):
    """Sends the scan report to Telegram as a file."""
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    
    with open(file_path, "rb") as file:
        files = {"document": file}
        payload = {"chat_id": chat_id, "caption": "Wapiti Scan Report"}
        response = requests.post(url, data=payload, files=files)
    
    return response.json()

def run_multi_target_scan(targets_file):
    """Reads multiple targets from a file and runs Wapiti scans on them."""
    if not os.path.exists(targets_file):
        raise FileNotFoundError("Targets file not found!")

    with open(targets_file, "r") as f:
        targets = [line.strip() for line in f.readlines() if line.strip()]

    if not targets:
        raise ValueError("No valid targets found in the file.")

    report_files = []
    for url in targets:
        print(f"Scanning: {url}")
        try:
            report_file = run_wapiti(url)
            report_files.append(report_file)
        except Exception as e:
            print(f"Error scanning {url}: {e}")

    return report_files

if __name__ == "__main__":
    targets_file = "targets.txt"  # File containing multiple URLs to scan
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    try:
        # Run scans for multiple targets
        report_files = run_multi_target_scan(targets_file)

        # Send each report to Telegram
        for report_file in report_files:
            response = send_to_telegram(report_file, telegram_chat_id, telegram_token)
            print(f"Sent report for {report_file}: {response}")

    except Exception as e:
        print(f"Error: {e}")
