import os
import requests

def run_wapiti(target_url):
    # Run Wapiti scan
    os.system(f"wapiti -u {target_url} -o report.html")
    with open("report.html", "r") as f:
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
    telegram_token = "7637902284:AAH-cSUSlU15UpaCfxwop1iHuawtpOw-WY8"  # Replace with your bot token
    telegram_chat_id = "6664808265"  # Replace with your chat ID

    # Run Wapiti scan
    report = run_wapiti(target_url)

    # Send report to Telegram
    send_to_telegram(f"Wapiti Scan Report:\n{report}", telegram_chat_id, telegram_token)
