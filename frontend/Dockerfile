# # Use the official Streamlit image as base
# FROM oawofolu/streamlit

# Use the official Python image as base
FROM python:3.12.3

# Set working directory in the container
WORKDIR /app/frontend

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire frontend directory into the container
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "view.py"]
