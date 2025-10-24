import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
from faq_service import find_faq

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chatbot-ruddy-eight.vercel.app/"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    q: str

@app.post("/api/chat")
async def chat(query: Query):
    q = query.q.strip().lower()
    
    # Special case for "hii"
    if q == "hii":
        return {"source": "custom", "answer": "Hello! How can I help you today?"}
    
    # 1. Local FAQ
    matches = find_faq(q)
    if matches:
        return {"source": "local", "answer": matches[0]["answer"]}
    
    # 2. Gemini fallback
    if not GEMINI_API_KEY:
        return {"source": "none", "answer": "No answer found and GEMINI_API_KEY not set."}
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"You are an assistant for Gopal Code Buster. Question: {q}"
        )
        return {"source": "gemini", "answer": response.text}
    except Exception as e:
        return {"source": "error", "answer": str(e)}



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # 8000 for local dev
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)