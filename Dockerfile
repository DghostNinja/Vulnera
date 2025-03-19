FROM python:3.9-slim

# Install Wapiti
RUN pip install wapiti3

# Install additional dependencies for your script
RUN pip install requests

# Copy your script
COPY scan.py /scan.py

# Set the working directory
WORKDIR /

# Run the script
CMD ["python", "scan.py"]
