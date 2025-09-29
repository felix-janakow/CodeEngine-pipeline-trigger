FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install the dependencies directly
RUN pip install requests>=2.25.0 boto3>=1.26.0

# Copy the source code
COPY ce-trigger-job.py .

# Define the command to run the script
CMD ["python", "ce-trigger-job.py"]