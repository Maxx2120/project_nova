from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database, auth, model_manager
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Chat"])

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FALLBACK_MODEL = "gemini-pro"  # Using Gemini for chat

@router.post("", response_model=schemas.ChatResponse)
async def chat(request: schemas.ChatRequest, 
               current_user: models.User = Depends(auth.get_current_user),
               db: Session = Depends(database.get_db)):
    
    # Save user message
    user_msg = models.ChatHistory(user_id=current_user.id, message=request.message, role="user")
    db.add(user_msg)
    db.commit()
    
    # Call Gemini API
    try:
        # Default model
        model_name = "gemini-2.5-flash"
        
        # Check if user requested a specific valid model
        if request.model and request.model.lower() != "string" and "llama" not in request.model.lower():
             model_name = request.model
             
        # Map legacy/unavailable models to valid ones for this key
        if model_name in ["gemini-pro", "gemini-1.5-flash", "mistral"]:
            model_name = "gemini-2.5-flash"
        
        logger.info(f"Using model: {model_name}")
        
        # We need to instantiate the specific model requested
        # The global one in model_manager might be different
        import google.generativeai as genai
        # Reuse configuration from manager if possible, but safe to re-configure or just use implicit
        model = genai.GenerativeModel(model_name)
        
        logger.info(f"Generating response for prompt: {request.message}")
        
        # Standard google-generativeai call
        response = model.generate_content(request.message)
        ai_text = response.text
        
        logger.info(f"Response generated successfully")
            
    except ValueError as e:
        ai_text = (
            f"Error: Gemini API not configured. "
            f"Set GEMINI_API_KEY environment variable. "
            f"Get your key from: https://makersuite.google.com/app/apikey"
        )
        logger.error(f"Gemini configuration error: {e}")
    except Exception as e:
        ai_text = f"Error generating response: {str(e)}"
        logger.error(f"Chat generation error: {e}")
    
    # Save AI response
    ai_msg = models.ChatHistory(user_id=current_user.id, message=ai_text, role="assistant")
    db.add(ai_msg)
    db.commit()
    
    return {"id": ai_msg.id, "user_id": ai_msg.user_id, "message": ai_msg.message, "role": ai_msg.role, "timestamp": ai_msg.timestamp}

@router.get("/history", response_model=list[schemas.ChatResponse])
def get_chat_history(current_user: models.User = Depends(auth.get_current_user),
                     db: Session = Depends(database.get_db)):
    return db.query(models.ChatHistory).filter(models.ChatHistory.user_id == current_user.id).all()

@router.get("/models")
async def get_models():
    """Return available chat models"""
    if GEMINI_API_KEY:
        # Based on available models for this key
        return {
            "models": [
                "gemini-2.5-flash", 
                "gemini-2.5-pro", 
                "gemini-2.0-flash", 
                "gemini-flash-latest"
            ], 
            "source": "Google Gemini"
        }
    else:
        return {
            "models": [FALLBACK_MODEL],
            "error": "GEMINI_API_KEY not configured",
            "note": "Get your API key from: https://makersuite.google.com/app/apikey"
        }
