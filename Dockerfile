FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY ce-trigger-job.py .

# Define the command to run the script
CMD ["python3", "ce-trigger-job.py"]