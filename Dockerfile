FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install the dependencies
RUN pip install requests

# Copy the source code
COPY ce_trigger_job.py .

# Define the command to run the script
CMD ["python", "ce_trigger_job.py"]