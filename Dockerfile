# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 7860 (Hugging Face default)
EXPOSE 7860

# Run the Flask app
CMD ["python", "app.py"]
