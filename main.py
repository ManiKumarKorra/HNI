import time
import openai
import os
from dotenv import load_dotenv
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import logging
import customer_intent

from transformers import pipeline

import warnings
 
# Ignore all warnings
warnings.filterwarnings("ignore")
# Load the .env file
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Assistant ID
ASSISTANT_ID = os.getenv("ASSISTANT_ID")


# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("transformers").setLevel(logging.ERROR)

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

whole_connversation = {}
whole_connversation["isthereconvo"]= False
print("whole conversation outside", whole_connversation['isthereconvo'] )
print(f"this is from outside {whole_connversation}")
@app.websocket("/communicate/{client_id}/{role}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, role: str):
    global check_connected_with_human  # Added this line to make `check_connected_with_human` global
    await manager.connect(websocket, role)
    session_active = True
    print(f"client id is {client_id}")
    try:
        if role == "customer":
            await manager.send_personal_message(
                "Hello! Welcome to HNI. We're here to offer creative solutions for your work and living spaces. How can I assist you today?", websocket
            )
        else:
            await manager.send_personal_message("Have a productive day!", websocket)

        while session_active:
            data = await websocket.receive_text()
            if role == "customer":
                intent = customer_intent.identify_intent(data)
                print("intent from websocket", intent)
                sentiment  = analyze_sentiment(data)
                print("sentiment in websocket", sentiment)
                if intent == "connect_with_human" or sentiment =='NEGATIVE':
          
                    # await manager.broadcast("summary",websocket)
                    # await manager.broadcast(f"Operator {client_id}: {data}", websocket)
                        
                    print("calling connect with human")
                    check_connected_with_human = True  # Now modifying the global variable
                    await connect_with_human(websocket, client_id, check_connected_with_human)
                    session_active = False

                else:
                    bot_response = await chat_with_bot(data)
                    await manager.send_personal_message(bot_response, websocket)
            elif role == "operator":
                if check_connected_with_human:
                    await manager.broadcast(f"Operator {data}", websocket)
                else:
                    print("nope")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast(f"Operator {client_id} has disconnected.", websocket)


async def connect_with_human(websocket: WebSocket, client_id: int, check_connected_with_human):

    """Handle transition to human operator."""
    await manager.send_personal_message("You are now chatting with a live representative.", websocket)
    await manager.broadcast(f"Customer {client_id} has requested to speak with an operator.", websocket)
    await manager.broadcast("Connection successful with the customer chat. Please proceed.",websocket)
    print(f"this message is from connect with humn function {whole_connversation}")
    await manager.broadcast(f"summary :",websocket)
    

    if whole_connversation["isthereconvo"]:
            index = 0       
            for message in reversed(whole_connversation['whole_data'].data):  
                print(f"Message ID: {message.id}")
                
                for content_block in reversed(message.content):  # Loop through the content list in reverse
                    if hasattr(content_block, 'text'):  # Check if 'text' attribute exists
                        print(f"Content Value: {content_block.text.value}")
                        
                        
                        if index % 2 == 0:
                            await manager.broadcast(f"user : {content_block.text.value}", websocket)
                        else:
                            await manager.broadcast(f"Bot : {content_block.text.value}", websocket)
                            
                        index += 1
    else:
        await manager.broadcast("no previous conversation", websocket)


            
    # await manager.broadcast(f"coversation {whole_connversation}",websocket)
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
                "Please respond to the user. Address them as a  HNI customer.Respond to the user in a professional and customer-focused manner. Avoid referencing data sources or providing source details. Write a clear, well-formatted, and readable response."
            )
        )
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            print("this is messages", messages)
           
            global whole_connversation
            
            whole_connversation['isthereconvo'] = True
            print("whole conversation", whole_connversation['isthereconvo'] )
            whole_connversation['whole_data'] = messages
            print(whole_connversation)
            print("inside function",whole_connversation)
            response = messages.data[0].content[0].text.value
            return response
        else:
            return "Bot is still processing..."
    except Exception as e:
        logging.error(f"Bot Error: {str(e)}")
        return "An error occurred. Please try again."
    
print(whole_connversation)
    


def analyze_sentiment(text: str) -> str:
 
    classifier = pipeline('sentiment-analysis')
 
    sentiment = classifier(text)
    print(f"result{sentiment}")
    # print(f"result{result}")
 
    return sentiment[0]['label']
 

 
 