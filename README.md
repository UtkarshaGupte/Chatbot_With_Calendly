# Calendly Chatbot with OpenAI Integration

## Overview

This project implements a chatbot using FastAPI, integrating with Calendly's API for scheduling events and OpenAI's GPT-3.5 model for natural language processing. The chatbot allows users to perform actions like listing their scheduled events and canceling specific events.

## Features

1. List Scheduled Events: Users can inquire about their upcoming events or appointments, and the chatbot retrieves the information from Calendly's API.
2. Cancel Event: Users can cancel a specific event by providing the date and time of the event they wish to cancel. The chatbot interacts with Calendly's API to perform the cancellation.
3. Natural Language Understanding: The chatbot utilizes OpenAI's GPT-3.5 model for natural language understanding, allowing users to interact with it using conversational language.

## Running the Backend:

1. Install dependencies:
` pip install -r requirements.txt `

2. Set up environment variables:
Create a .env file in the project directory.

Add the following environment variables:
CALENDLY_API_KEY=<your_calendly_api_key>
OPENAI_API_KEY=<your_openai_api_key>
MODEL=gpt-3.5-turbo-0125 

3. Navigate to the directory containing the backend file in your terminal or command prompt.

Run the FastAPI application using the uvicorn server by executing the following command: 
` uvicorn app:app --reload `

4. Once the backend server is running, it will listen for requests on http://127.0.0.1:8000


## Running the Frontend:

To run the frontend of the application, follow these steps:

1. Ensure you have Python installed on your system.
2. Install the required dependencies by running the following command in your terminal or command prompt:
 ` pip install streamlit requests `
3. Navigate to the directory containing the frontend file in your terminal or command prompt.
4. Run the Streamlit application by executing the following command:
` streamlit run view.py `
5. Once the application is running, you can access it by opening a web browser and visiting the URL provided in the terminal output (usually http://localhost:8501).




