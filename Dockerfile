# "start from a minimal, pre-built Linux image that already has Python 3.10 installed", 
#your actual foundation, matching the Python version you've been developing with.
FROM python:3.10-slim 

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies without saving cache to keep image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the API port
EXPOSE 800

CMD ["uvicorn", "app,main:app", "--host", "0.0.0", "--port", "8000"]