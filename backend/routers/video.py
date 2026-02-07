from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from .. import schemas, models, database, auth
import subprocess
import uuid
import os

router = APIRouter(tags=["Video Processing"])

@router.post("/video/upload", response_model=schemas.VideoResponse)
async def upload_video(file: UploadFile = File(...),
                       current_user: models.User = Depends(auth.get_current_user),
                       db: Session = Depends(database.get_db)):
    
    # Save the file
    upload_dir = "static/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{file.filename}"
    filepath = os.path.join(upload_dir, filename)
    
    with open(filepath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    task = models.VideoTask(user_id=current_user.id, prompt="Uploaded", source_video=filepath, status="pending")
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return schemas.VideoResponse(id=task.id, user_id=task.user_id, prompt=task.prompt, status=task.status, output_url=None, created_at=task.created_at)

@router.post("/video/process/{task_id}", response_model=schemas.VideoResponse)
def process_video(task_id: int, request: schemas.VideoRequest,
                  current_user: models.User = Depends(auth.get_current_user),
                  db: Session = Depends(database.get_db)):
    
    task = db.query(models.VideoTask).filter(models.VideoTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Video task not found")
    
    if task.user_id != current_user.id:
         raise HTTPException(status_code=403, detail="Not authorized")

    # Simple text-to-ffmpeg logic mapping
    prompt_lower = request.prompt.lower()
    filter_arg = ""
    
    if "black and white" in prompt_lower or "grayscale" in prompt_lower:
        filter_arg = "hue=s=0"
    elif "sepia" in prompt_lower:
        filter_arg = "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131"
    elif "mirror" in prompt_lower:
        filter_arg = "hflip"
    elif "reverse" in prompt_lower:
        filter_arg = "reverse"
    else:
        # Default fallback or error
        filter_arg = "eq=brightness=0.06:saturation=2" # cinematic "pop" default

    output_filename = f"processed_{os.path.basename(task.source_video)}"
    output_path = os.path.join("static/processed", output_filename)
    os.makedirs("static/processed", exist_ok=True)
    
    try:
        command = [
            "ffmpeg", "-y", "-i", task.source_video, "-vf", filter_arg, output_path
        ]
        subprocess.run(command, check=True)
        
        task.output_video = output_path
        task.status = "completed"
        task.prompt = request.prompt
        db.commit()
        db.refresh(task)
        
        return schemas.VideoResponse(id=task.id, user_id=task.user_id, prompt=task.prompt, status=task.status, output_url=f"/static/processed/{output_filename}", created_at=task.created_at)
        
    except subprocess.CalledProcessError as e:
        task.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
