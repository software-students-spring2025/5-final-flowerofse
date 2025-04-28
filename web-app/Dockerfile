FROM python:3.10-slim

# Install system packages
RUN apt-get update && apt-get install -y build-essential gcc

# Set working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=3001"]