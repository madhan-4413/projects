import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Voice Agent Backend",
    description="Webhook server to handle tool calls and conversation events from Vapi.ai",
    version="1.0.0"
)

# In-memory mock database for illustration
MOCK_APPOINTMENTS = {
    "12345": {"name": "Alice Smith", "time": "2:30 PM", "status": "Confirmed", "service": "Dental Cleaning"},
    "67890": {"name": "Bob Jones", "time": "10:00 AM", "status": "Pending", "service": "Consultation"}
}

@app.get("/")
def read_root():
    return {"status": "online", "message": "Voice agent webhook server is running."}

@app.post("/webhook")
async def handle_vapi_webhook(request: Request):
    """
    Primary endpoint for Vapi.ai webhooks and tool calls.
    Vapi sends POST requests here when the assistant triggers a custom tool.
    """
    try:
        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    message = payload.get("message", {})
    message_type = message.get("type")

    # Log the incoming event type
    print(f"Received Vapi webhook event: {message_type}")

    # Check if this is a tool-calls event
    if message_type == "tool-calls":
        tool_calls_list = message.get("toolCalls", [])
        
        # If 'toolCalls' is missing, fallback to single 'toolCall'
        if not tool_calls_list and "toolCall" in message:
            tool_calls_list = [message["toolCall"]]
            
        results = []
        for tool_call in tool_calls_list:
            tool_id = tool_call.get("id")
            function_data = tool_call.get("function", {})
            function_name = function_data.get("name")
            arguments = function_data.get("arguments", {})

            print(f"Executing tool '{function_name}' with arguments: {arguments}")
            
            # Route to the appropriate function logic
            if function_name == "check_appointment_status":
                appointment_id = arguments.get("appointment_id")
                result_data = check_appointment_status(appointment_id)
            elif function_name == "book_appointment":
                name = arguments.get("name")
                time = arguments.get("time")
                service = arguments.get("service")
                result_data = book_appointment(name, time, service)
            else:
                result_data = f"Error: Tool '{function_name}' is not recognized by the backend."

            results.append({
                "toolCallId": tool_id,
                "result": result_data
            })

        # Return the response structure that Vapi expects
        return JSONResponse(content={"results": results})

    # Other events Vapi sends during a call:
    # - "speech-update": Real-time transcripts
    # - "transcript": Final transcript of the conversation
    # - "status-update": Call status changes (e.g. ringing, connected, ended)
    # - "hang": Triggered when the call ends
    elif message_type == "status-update":
        call_status = message.get("status")
        print(f"Call status updated: {call_status}")
        return {"status": "acknowledged"}

    elif message_type == "hang":
        print("Call hung up. Recording final summary...")
        return {"status": "acknowledged"}

    return {"status": "ignored", "event_received": message_type}


# --- Tool Implementation Functions ---

def check_appointment_status(appointment_id: str) -> dict:
    """Check appointment status in the mock database."""
    if not appointment_id:
        return {"error": "Missing appointment_id"}
        
    appointment = MOCK_APPOINTMENTS.get(str(appointment_id))
    if appointment:
        return {
            "found": True,
            "appointment_id": appointment_id,
            "client_name": appointment["name"],
            "time": appointment["time"],
            "status": appointment["status"],
            "service": appointment["service"]
        }
    return {
        "found": False,
        "message": f"No appointment found with ID {appointment_id}."
    }

def book_appointment(name: str, time: str, service: str) -> dict:
    """Create a new mock appointment booking."""
    if not name or not time or not service:
        return {"error": "Missing required fields (name, time, service)"}
        
    # Generate a simple mock ID
    new_id = str(len(MOCK_APPOINTMENTS) + 12345)
    MOCK_APPOINTMENTS[new_id] = {
        "name": name,
        "time": time,
        "status": "Confirmed",
        "service": service
    }
    
    return {
        "success": True,
        "appointment_id": new_id,
        "message": f"Appointment successfully booked for {name} on {time} for {service}."
    }

if __name__ == "__main__":
    import uvicorn
    # Start the server on port 8000
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
