# Use an official Python runtime
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies globally (no venv)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5003

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=dev
ENV PYTHONUNBUFFERED=1

# Start the application using Waitress (production) or Flask (development)
# CMD ["waitress-serve", "--host=0.0.0.0", "--port=5003", "app:app"]

# Uncomment for development mode
CMD ["flask", "run", "--host=0.0.0.0", "--port=5003", "--debug"]