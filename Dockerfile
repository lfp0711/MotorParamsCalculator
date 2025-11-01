FROM python:3.13

# Set working directory
WORKDIR /app

# Install build deps (some libraries may need build tools)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install requirements. If requirements file contains non-standard lines this will fall back
# to installing common dependencies used by this project.
RUN pip install --upgrade pip \
    && pip install -r requirements.txt || pip install Flask numpy bootstrap-flask Flask-CKEditor flask-csrf Flask-DebugToolbar Flask-FileUpload

# Copy the rest of the project
COPY . /app

# Expose the default Flask port
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]
