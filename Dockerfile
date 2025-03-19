# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY scan.py targets.txt requirements.txt ./

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Wapiti scanner
RUN apt update && apt install -y wapiti

# Expose necessary ports (optional, if you plan to add a web UI later)
EXPOSE 8080

# Set environment variables for Telegram Bot (These can be set at runtime)
ENV TELEGRAM_TOKEN=""
ENV TELEGRAM_CHAT_ID=""

# Run the scan when the container starts
CMD ["python", "scan.py"]
