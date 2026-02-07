from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database, auth
try:
    import torch
except ImportError:
    torch = None
from pathlib import Path

router = APIRouter(tags=["Image Generation"])

# Placeholder for the pipeline
pipe = None
MODEL_ID = "runwayml/stable-diffusion-v1-5" # Or a local path

def load_model():
    global pipe
    try:
        from diffusers import StableDiffusionPipeline
        # Attempt to load model - this might be slow or fail on low RAM
        # Using float32 for CPU compatibility if GPU not available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        
        # NOTE: This requires the model to be downloaded locally or cached
        pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=dtype)
        pipe.to(device)
        if device == "cpu":
            pipe.enable_attention_slicing() # optimization for low RAM
    except Exception as e:
        print(f"Warning: Could not load Stable Diffusion model: {e}")

# Trigger model load on startup or first request (lazy load)
# load_model() 

@router.post("/image/generate", response_model=schemas.ImageResponse)
def generate_image(request: schemas.ImageRequest,
                   current_user: models.User = Depends(auth.get_current_user),
                   db: Session = Depends(database.get_db)):
    
    global pipe
    if pipe is None:
        try:
            load_model()
        except:
             pass

    if pipe is None:
        # Fallback for testing/if model fails to load
        raise HTTPException(status_code=500, detail="Image model not loaded. Please check server logs.")

    try:
        image = pipe(request.prompt).images[0]
        
        # Save image
        filename = f"{current_user.id}_{request.prompt[:10].replace(' ', '_')}.png"
        output_dir = Path("static/generated_images")
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / filename
        image.save(filepath)
        
        # Save to DB
        db_image = models.ImagePrompt(user_id=current_user.id, prompt=request.prompt, image_path=str(filepath))
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        return schemas.ImageResponse(id=db_image.id, prompt=db_image.prompt, image_url=f"/static/generated_images/{filename}", created_at=db_image.created_at)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
