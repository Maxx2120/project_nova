from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database, auth
import requests

router = APIRouter(tags=["Chat"])

OLLAMA_URL = "http://localhost:11434/api/generate"

@router.post("/chat", response_model=schemas.ChatResponse)
async def chat(request: schemas.ChatRequest, 
               current_user: models.User = Depends(auth.get_current_user),
               db: Session = Depends(database.get_db)):
    
    # Save user message
    user_msg = models.ChatHistory(user_id=current_user.id, message=request.message, role="user")
    db.add(user_msg)
    db.commit()
    
    # Call Ollama
    try:
        payload = {
            "model": request.model,
            "prompt": request.message,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload)
        ai_text = response.json().get("response", "Error processing request")
    except Exception as e:
        ai_text = f"Error connecting to Ollama: {str(e)}"
    
    # Save AI response
    ai_msg = models.ChatHistory(user_id=current_user.id, message=ai_text, role="assistant")
    db.add(ai_msg)
    db.commit()
    
    return {"id": ai_msg.id, "user_id": ai_msg.user_id, "message": ai_msg.message, "role": ai_msg.role, "timestamp": ai_msg.timestamp}

@router.get("/chat/history", response_model=list[schemas.ChatResponse])
def get_chat_history(current_user: models.User = Depends(auth.get_current_user),
                     db: Session = Depends(database.get_db)):
    return db.query(models.ChatHistory).filter(models.ChatHistory.user_id == current_user.id).all()
