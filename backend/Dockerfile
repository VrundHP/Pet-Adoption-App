FROM python:latest

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Initialize database
RUN python database.py

# Expose the port for Flask
EXPOSE 5000

# Run the Flask app with proper environment variables
CMD ["python3", "main.py", "--host=0.0.0.0", "--port=5000"]
