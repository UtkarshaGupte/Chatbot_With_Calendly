# Use the official Python image as base
FROM python:3.12.3

# Set environment variables
ENV CALENDLY_API_KEY=eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzEzNDY1MDEzLCJqdGkiOiIyYTMyYjQxZi1kNTI0LTRhZjctOThhMS04YTFlNzA1NmEyYjgiLCJ1c2VyX3V1aWQiOiJiNmE1Yzc4OS1iMWNkLTQxOGUtYmJhZC1lMWY4YjNhNWM0YjAifQ.3R2dqrP0uhrKWCIFqz9H8WzobOmEZ0J1lqUt65kXj6liTQ73cnUDP5gswaqRuYBal8xtqNdEgRC1GUfz3aJGQw
ENV OPENAI_API_KEY=sk-proj-57CIXWuKBWZfDTiTJuyaT3BlbkFJH5TCfLKuFtFtMd3ilDbg
ENV MODEL=gpt-3.5-turbo-0125

# Set working directory in the container
WORKDIR /app/backend

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory into the container
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]