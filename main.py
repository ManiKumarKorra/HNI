import time
import openai
import os
from dotenv import load_dotenv
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import logging
import customer_intent
from textblob import TextBlob
# test commit
# Load the .env file
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Assistant ID
ASSISTANT_ID = os.getenv("ASSISTANT_ID")


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
app = FastAPI()

class ConnectionManager:
    """Manage WebSocket connections."""
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.operators: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, role: str):
        await websocket.accept()
        if role == "operator":
            self.operators.append(websocket)
        else:
            self.active_connections.append(websocket)
        logging.info(f"Connected: {role}")

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.operators:
            self.operators.remove(websocket)
        else:
            self.active_connections.remove(websocket)
        logging.info("Disconnected")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        logging.info(f"Sent personal message: {message}")

    async def broadcast(self, message: str, sender: WebSocket):
        for connection in self.active_connections + self.operators:
            if connection != sender:
                await connection.send_text(message)
        logging.info(f"Broadcast message: {message}")

manager = ConnectionManager()

@app.get("/")
async def get_customer():
    return FileResponse('customer.html')

@app.get("/operator")
async def get_operator():
    return FileResponse('operator.html')

@app.get("/styles.css")
async def get_styles():
    return FileResponse('styles.css')

check_connected_with_human = False

@app.websocket("/communicate/{client_id}/{role}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, role: str):
    global check_connected_with_human  # Added this line to make `check_connected_with_human` global
    await manager.connect(websocket, role)
    session_active = True
    print(f"client id is {client_id}")
    try:
        if role == "customer":
            await manager.send_personal_message(
                "Greetings! At HNI, we’re here to provide innovative solutions for your work and living spaces. How may we assist you?", websocket
            )
        else:
            await manager.send_personal_message("Have a productive day!", websocket)

        while session_active:
            data = await websocket.receive_text()
            if role == "customer":
                intent = customer_intent.identify_intent(data)
                sentiment  = analyze_sentiment(data)
                if intent == "connect_with_human" or sentiment =='angry':
                    if sentiment =='angry':
                        await manager.send_personal_message("we noticed that you are upset", websocket)
                        
                    print("calling connect with human")
                    check_connected_with_human = True  # Now modifying the global variable
                    await connect_with_human(websocket, client_id, check_connected_with_human)
                    session_active = False

                else:
                    bot_response = await chat_with_bot(data)
                    await manager.send_personal_message(bot_response, websocket)
            elif role == "operator":
                if check_connected_with_human:
                    await manager.broadcast(f"Operator {client_id}: {data}", websocket)
                else:
                    print("nope")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast(f"{client_id} user has disconnected.", websocket)


async def connect_with_human(websocket: WebSocket, client_id: int, check_connected_with_human):

    """Handle transition to human operator."""
    await manager.send_personal_message("You are now connected with a human operator", websocket)
    await manager.broadcast(f"Customer {client_id} requested for a connect with an operator.", websocket)
    await manager.broadcast("customer is connected",websocket)
    print(f"this is client_id{client_id}")

    try:
        while True:
            data = await websocket.receive_text()
            message = f"Customer {client_id}: {data}" if websocket in manager.active_connections else f"Operator {client_id}: {data}"
            
            await manager.broadcast(message, websocket)
            print("opeator message", message)
            
            # await manager.send_personal_message("not connected with any customer", websocket)

            
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast(f"{client_id} has disconnected.", websocket)

async def chat_with_bot(data: str) -> str:
    """Run the bot logic asynchronously."""
    return await asyncio.to_thread(chat_with_bot_sync, data)


client = openai.OpenAI()
thread = client.beta.threads.create()
print("Initializing chat thread...")
print(f"Thread initialized: {thread.id}")

def chat_with_bot_sync(data: str) -> str:
    """Synchronous bot logic."""
    try:
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=data
        )
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID,
            instructions=(
                "Please respond to the user. Address them as a valuable HNI customer. do not disclose the data where  you are getting from like which data source .txt   and text should be neat and clean readable"
                
            )
        )
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            print(f"this is a tread messae{messages}")
            response = messages.data[0].content[0].text.value
            return response
        else:
            return "Bot is still processing..."
    except Exception as e:
        logging.error(f"Bot Error: {str(e)}")
        return "An error occurred. Please try again."
    


def analyze_sentiment(text: str) -> str:
   
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity < 1:  # Adjust threshold as needed
        return "angry"
    return "normal"
