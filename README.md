# Vulnera - Automated DAST Scanner for CI/CD Pipelines

![Vulnra Banner](assets/vulnera.jpg)


## 🚀 Introduction
**Vulnera** is a lightweight yet powerful **Dynamic Application Security Testing (DAST)** tool designed for **startups and DevSecOps teams**. It seamlessly integrates into **CI/CD pipelines**, allowing automated security scanning of web applications to detect vulnerabilities before deployment.

🔍 **Key Features:**
- **Automated web application security scanning** using [Wapiti](http://wapiti.sourceforge.net/)
- **CI/CD integration** for continuous security monitoring
- **Multi-target scanning** from a list of URLs
- **Real-time vulnerability reports** sent directly to Telegram
- **Docker support** for easy deployment across environments
- **GitHub Actions support** for scheduled and on-push scans

## 📦 Installation & Setup
You can run **Vulnera** on your local machine, in a CI/CD pipeline, or within a Docker container.

### **1️⃣ Cloning the Repository**
```sh
# Clone the repository
git clone https://github.com/DghostNinja/Vulnera.git
cd Vulnra
```

### **2️⃣ Install Dependencies (For Manual Execution)**
Ensure you have Python and Wapiti installed.
```sh
# Install Python dependencies
pip install -r requirements.txt

# Install Wapiti (Debian/Ubuntu)
sudo apt update && sudo apt install -y wapiti
```

## 🚀 Running Vulnera 
### **Single Target Scan (Manual Execution)**
```sh
python scan.py
```

### **Multi-Target Scan**
Add multiple URLs to `targets.txt` (one per line) and run:
```sh
python scan.py targets.txt
```

---
## 🐳 Running Vulnera with Docker
### **1️⃣ Build the Docker Image**
```sh
docker build -t vulnra .
```

### **2️⃣ Run a Single Target Scan**
```sh
docker run --rm \
  -e TELEGRAM_TOKEN="your_telegram_bot_token" \
  -e TELEGRAM_CHAT_ID="your_chat_id" \
  vulnra
```

### **3️⃣ Run a Multi-Target Scan**
```sh
docker run --rm \
  -v "$(pwd)/targets.txt:/app/targets.txt" \
  -e TELEGRAM_TOKEN="your_telegram_bot_token" \
  -e TELEGRAM_CHAT_ID="your_chat_id" \
  vulnra
```

---
## 🛠️ CI/CD Integration with GitHub Actions
Vulnra can be integrated into a **GitHub Actions workflow** to automate security testing on every push.

### **Add the following to `.github/workflows/main.yml`**
```yaml
name: DAST Security Scan

on:
  push:
    branches:
      - main
  schedule:
    - cron: "0 0 * * *"  # Runs daily at midnight

jobs:
  dast_scan:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Cache Wapiti
        id: cache-wapiti
        uses: actions/cache@v4
        with:
          path: /usr/bin/wapiti
          key: wapiti-cache-v1
          restore-keys: wapiti-cache-

      - name: Install Wapiti (if not cached)
        if: steps.cache-wapiti.outputs.cache-hit != 'true'
        run: |
          sudo apt update
          sudo apt install -y wapiti

      - name: Install Python Dependencies
        run: pip install requests

      - name: Run Wapiti Scan and Send Report
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python scan.py
```

---
## 📬 Telegram Alerts
Vulnra sends scan reports **directly to Telegram** for real-time monitoring.

🔹 **Create a Telegram Bot** using [BotFather](https://t.me/BotFather).  
🔹 **Get your Chat ID** from [IDBot](https://t.me/myidbot).  
🔹 Set up **GitHub Secrets** for:
  - `TELEGRAM_TOKEN`
  - `TELEGRAM_CHAT_ID`

---
## 📜 License
This project is licensed under the **MIT License**.

---
## 🎯 Future Enhancements
- 📌 **Advanced reporting** (PDF, JSON, CSV)
- 📌 **Webhook support** for alerting integrations
- 📌 **AI-based risk classification**

Contributions are welcome! 🚀 **PRs & Issues** are encouraged.

---
## ✨ Author
Developed by **iPsalmy** (@DghostNinja) for **startups & security-conscious developers**. 🛡️

