from dotenv import load_dotenv
import os
import requests


from fastapi import FastAPI, Request

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("CALENDLY_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
MODEL =  os.getenv("MODEL")


# Define functions to interact with the Calendly API

# Function 1: List Scheduled Events
@tool
def list_scheduled_events():
    """List the user's scheduled events from Calendly. Use this tool when the user asks to see their upcoming events or scheduled appointments."""
    try:
        url = "https://api.calendly.com/scheduled_events"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        params = {
            "organization": "https://api.calendly.com/organizations/11a908ed-35ec-4bf7-a01f-25fc68505548",
            "user": "https://api.calendly.com/users/b6a5c789-b1cd-418e-bbad-e1f8b3a5c4b0"
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors
        error_message = e.response.json().get("message", "Unknown error")
        return {"error": error_message}
    except Exception as e:
        # Handle the error gracefully
        return {"error": str(e)}


# Function 2: Cancel an Event
@tool
def cancel_event(date, time):
    """Cancel an event in Calendly based on the provided time and date. Use this tool when the user wants to cancel a specific scheduled event, typically by providing some details about the event like date, time, or description."""
    try:
        # Get list of scheduled events
        url = "https://api.calendly.com/scheduled_events"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        params = {
            "organization": "https://api.calendly.com/organizations/11a908ed-35ec-4bf7-a01f-25fc68505548",
            "user": "https://api.calendly.com/users/b6a5c789-b1cd-418e-bbad-e1f8b3a5c4b0"
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        scheduled_events = response.json()
        

        # Find the event with matching time and date
        event_uuid = None
        for event in scheduled_events['collection']:

            if event["status"] == "active":
                event_time = event["start_time"]
                event_date = event_time.split("T")[0]  # Extract date from start_time
                time_str = event_time.split("T")[1].split(":")[0] + ":" + event_time.split("T")[1].split(":")[1]  # Extract hour:min from start_time
                if event_date == date and time_str == time:
                    event_uuid = event["uri"]
                    event_uuid = event_uuid.split("/")[-1]
                    break
   
        if event_uuid:
            url = f"https://api.calendly.com/scheduled_events/{event_uuid}/cancellation"
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            return response.json()
        else:
            # Event not found, return error message
            return {"error": "Event not found"}

              
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors
        error_message = e.response.json().get("message", "Unknown error")
        return {"error": error_message}
    except Exception as e:
        # Handle the error gracefully
        return {"error": str(e)}
    

# Define tools for the Langchain agent
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_scheduled_events",
            "description": "List the user's scheduled events from Calendly. Use this tool when the user asks to see their upcoming events or scheduled appointments.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }
    },
        {
            "type": "function",
            "function": {
                "name": "cancel_event",
                "description": "Cancel an event in Calendly. Use this tool when the user wants to cancel a specific scheduled event, typically by providing a description like 'cancel my event at 3pm today'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                        "type": "string",
                        "format": "date",
                        "description": "The date of the event to cancel. If the user provides a relative day description like 'today', 'tomorrow', or a specific day (e.g., 'Monday'), convert it to the proper date format (YYYY-MM-DD) relative to the current date. Todays date is 18 April 2024"
                    },
                    "time": {
                        "type": "string",
                        "format": "time",
                        "description": "The time of the event to cancel. If they specify the time in any format, convert it  to the 24-hour format."
                    }
                    },
                    "required": ["date", "time"],
                },
            }
    },
]

# This is the model I am using - gpt-3.5-turbo-0125
llm = ChatOpenAI(model=MODEL, api_key=openai_api_key)
llm_with_tools = llm.bind_tools(tools)


app = FastAPI()
@app.post("/chatbot")
async def chatbot_endpoint(request: Request):
    data = await request.json()
    message =  data["message"]
    # Create a HumanMessage object with the user's input
    messages = [HumanMessage(message)]
    ai_msg = llm_with_tools.invoke(messages)

    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        selected_tool = {"list_scheduled_events": list_scheduled_events, "cancel_event": cancel_event}[tool_call["name"].lower()]
        tool_output = selected_tool.invoke(tool_call["args"])

        # Convert tool_output to a string or a list
        if isinstance(tool_output, dict) or isinstance(tool_output, list):
            tool_output = str(tool_output)
        elif not isinstance(tool_output, str):
            tool_output = [str(tool_output)]

        messages.append(ToolMessage(content=tool_output, tool_call_id=tool_call["id"]))
    
    bot_response = llm_with_tools.invoke(messages)

    # Return the bot's response
    return {"response": bot_response}


# ========= Testing =============
# query1 = "show me the scheduled events"
# res1 = llm_with_tools.invoke(query1).tool_calls
# print(res1)

# query2 = "cancel my event at 3pm today"
# res2 = llm_with_tools.invoke(query2).tool_calls
# print(res2)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)