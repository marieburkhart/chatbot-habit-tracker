from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os

# Load OpenAI API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create FastAPI app
app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all; tighten this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request body
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(chat: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": chat.message}],
            temperature=0.7
        )
        reply = response.choices[0].message['content'].strip()
        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}