# AI Voice Agent Backend

This is a Python-based FastAPI backend server designed to handle Webhooks and Custom Tool Calls (Function Calling) from a managed voice platform like **[Vapi.ai](https://vapi.ai)**.

By connecting Vapi to this server, your voice agent can dynamically retrieve real-time data (e.g., checking database records) or execute actions (e.g., booking appointments) mid-conversation based on what the user says.

---

## 🚀 Setup & Execution

### 1. Install Dependencies
Make sure you have Python 3.8+ installed. Navigate to this directory and install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Run the Server Locally
Launch the FastAPI development server:
```bash
python app.py
```
By default, the server will start running at `http://localhost:8000`. 
- Open `http://localhost:8000/` in your browser to verify it's active.
- Open `http://localhost:8000/docs` to view the interactive Swagger API documentation.

### 3. Expose Your Local Server to the Internet (For Testing)
Vapi needs a public URL to send webhooks to. You can use **ngrok** to temporarily expose your localhost:
```bash
ngrok http 8000
```
Copy the forwarding HTTPS URL provided by ngrok (e.g., `https://xxxx-xx-xx.ngrok-free.app`). Your webhook endpoint will be `https://xxxx-xx-xx.ngrok-free.app/webhook`.

---

## 🛠️ Linking to Vapi.ai Dashboard

To hook this server up to your Vapi agent:

### Step A: Define the Custom Tool in Vapi
1. Go to the **Vapi Dashboard** -> **Tools** -> **Create Tool**.
2. Set the type to **Function**.
3. Fill in the tool configuration:
   - **Name**: `check_appointment_status`
   - **Description**: "Checks the status of an appointment using a unique 5-digit appointment ID."
   - **Parameters (JSON Schema)**:
     ```json
     {
       "type": "object",
       "properties": {
         "appointment_id": {
           "type": "string",
           "description": "The 5-digit appointment reference number (e.g., 12345)."
         }
       },
       "required": ["appointment_id"]
     }
     ```
   - **Server URL**: Enter your Ngrok webhook URL: `https://xxxx-xx-xx.ngrok-free.app/webhook`

### Step B: Attach Tool to Assistant
1. Go to **Assistants** in the dashboard.
2. Select your voice agent.
3. Under the **Tools** section, add/enable the `check_appointment_status` tool you just created.
4. Give your assistant instructions (system prompt) explaining when and how to use it:
   > "You are a customer service assistant. If a user asks about their appointment status, ask them for their 5-digit appointment ID. Once they give it to you, call the `check_appointment_status` tool to look it up, and tell them the status."
