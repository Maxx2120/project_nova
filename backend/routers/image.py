from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database, auth, model_manager
from pathlib import Path
import logging
import torch

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Image Generation"])

@router.post("/generate", response_model=schemas.ImageResponse)
def generate_image(request: schemas.ImageRequest,
                   current_user: models.User = Depends(auth.get_current_user),
                   db: Session = Depends(database.get_db)):
    
    output_dir = Path("static/generated_images")
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{current_user.id}_{request.prompt[:10].replace(' ', '_')}.png"
    filepath = output_dir / filename

    try:
        # Get the pipeline
        pipe = model_manager.get_stable_diffusion_pipeline()
        
        if pipe is None:
            raise HTTPException(
                status_code=503, 
                detail="Stable Diffusion model not available. Run setup_models.py first."
            )
        
        # Generate image with optimized steps for LCM
        logger.info(f"Generating image for prompt: {request.prompt}")
        if pipe.device.type == 'cpu':
            # LCM uses much fewer steps for fast inference (4-8 steps)
            steps = 4  # LCM can generate good results in just 4 steps
        else:
            steps = 6  # GPU can use slightly more for better quality
            
        image = pipe(request.prompt, num_inference_steps=steps).images[0]
        image.save(filepath)
        logger.info(f"Image saved to {filepath}")
        
    except torch.cuda.OutOfMemoryError:
        logger.error("GPU out of memory")
        raise HTTPException(
            status_code=503,
            detail="GPU out of memory. Please try again or use CPU mode."
        )
    except Exception as e:
        logger.error(f"Image generation error: {e}")
        # Fallback: Create a placeholder image
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (512, 512), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            text = f"Generation Error\n{str(e)[:30]}\nPrompt: {request.prompt[:20]}"
            d.text((10, 10), text, fill=(255, 255, 0))
            img.save(filepath)
            logger.info(f"Placeholder image created for error handling")
        except:
            raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")
        
    # Save to DB
    db_image = models.ImagePrompt(user_id=current_user.id, prompt=request.prompt, image_path=str(filepath))
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    
    return schemas.ImageResponse(id=db_image.id, prompt=db_image.prompt, image_url=f"/static/generated_images/{filename}", created_at=db_image.created_at)
