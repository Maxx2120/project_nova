from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# USER
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

# CHAT
class ChatMessage(BaseModel):
    role: str
    content: str
    
class ChatRequest(BaseModel):
    message: str
    model: str = "mistral"
    
class ChatResponse(BaseModel):
    id: int
    user_id: int
    message: str
    role: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

# IMAGE
class ImageRequest(BaseModel):
    prompt: str
    width: int = 512
    height: int = 512
    
class ImageResponse(BaseModel):
    id: int
    prompt: str
    image_url: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# VIDEO
class VideoRequest(BaseModel):
    prompt: str
    
class VideoResponse(BaseModel):
    id: int
    user_id: int
    prompt: str
    status: str
    output_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
