"""
Model initialization and management for AI features
Supports both Gemini API and local models
"""

# import torch is moved inside functions to allow web server to start even if torch crashes on import
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)

# Global model instances
_stable_diffusion_pipeline = None
_gemini_model = None
_is_initialized = False


def initialize_models():
    """Initialize all AI models on startup"""
    global _is_initialized, _gemini_model, _stable_diffusion_pipeline
    
    if _is_initialized:
        return
    
    logger.info("Initializing AI models...")
    
    # Initialize Gemini
    try:
        load_gemini_model()
        logger.info("✓ Gemini API loaded")
    except Exception as e:
        logger.warning(f"Gemini API not available: {e}")
    
    # Try to load Stable Diffusion (fallback for images)
    try:
        load_stable_diffusion()
        logger.info("✓ Stable Diffusion loaded")
    except Exception as e:
        logger.warning(f"Stable Diffusion not available: {e}")
    
    _is_initialized = True


def load_gemini_model():
    """Load Google Gemini API"""
    global _gemini_model
    
    if _gemini_model is not None:
        return _gemini_model
    
    import google.genai as genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable not set. "
            "Get your key from https://makersuite.google.com/app/apikey"
        )
    
    genai.configure(api_key=api_key)
    
    # Initialize the model
    _gemini_model = genai.GenerativeModel('gemini-pro')
    
    logger.info(f"✓ Gemini API configured successfully")
    logger.info(f"  - Model: gemini-pro")
    logger.info(f"  - Type: Text generation (chat)")
    
    return _gemini_model


def get_gemini_model():
    """Get or load Gemini model"""
    global _gemini_model
    
    if _gemini_model is None:
        load_gemini_model()
    
    return _gemini_model


def load_stable_diffusion():
    """Load Stable Diffusion with LCM for CPU optimization"""
    global _stable_diffusion_pipeline
    
    if _stable_diffusion_pipeline is not None:
        return _stable_diffusion_pipeline
    
    try:
        import torch
    except Exception as e:
        logger.error(f"Failed to import torch: {e}")
        return None
    
    # Use LCM (Latent Consistency Model) for fast CPU inference
    # LCM can generate images in 5-10 steps instead of 50+
    try:
        from diffusers import LCMScheduler, StableDiffusionPipeline
        
        MODEL_ID = "runwayml/stable-diffusion-v1-5"
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        
        logger.info(f"Loading Stable Diffusion with LCM on {device} with dtype {dtype}...")
        
        _stable_diffusion_pipeline = StableDiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=dtype,
            safety_checker=None
        )
        
        # Replace scheduler with LCM for faster inference
        _stable_diffusion_pipeline.scheduler = LCMScheduler.from_config(
            _stable_diffusion_pipeline.scheduler.config
        )
        
        _stable_diffusion_pipeline = _stable_diffusion_pipeline.to(device)
        
        # Optimize for lower memory usage on CPU
        _stable_diffusion_pipeline.enable_attention_slicing()
        
        if device == "cpu":
            # CPU-specific optimizations
            logger.info("Applying CPU optimizations...")
            _stable_diffusion_pipeline.enable_attention_slicing()
            # Reduce precision for CPU
        elif device == "cuda":
            # Enable sequential cpu offload for lower VRAM usage
            try:
                _stable_diffusion_pipeline.enable_sequential_cpu_offload()
                logger.info("Enabled sequential CPU offload for VRAM optimization")
            except Exception as e:
                logger.warning(f"Could not enable CPU offload: {e}")
        
        logger.info(f"✓ Stable Diffusion with LCM ready on {device}")
        logger.info(f"  - Model: {MODEL_ID}")
        logger.info(f"  - Scheduler: LCM (fast inference, ~5-10 steps)")
        logger.info(f"  - Expected speed: 5-20 seconds per image on CPU")
        
    except ImportError:
        logger.warning("LCM not available, falling back to standard Stable Diffusion")
        try:
            from diffusers import StableDiffusionPipeline
            
            MODEL_ID = "runwayml/stable-diffusion-v1-5"
            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.float16 if device == "cuda" else torch.float32
            
            _stable_diffusion_pipeline = StableDiffusionPipeline.from_pretrained(
                MODEL_ID,
                torch_dtype=dtype,
                safety_checker=None
            )
            _stable_diffusion_pipeline = _stable_diffusion_pipeline.to(device)
            _stable_diffusion_pipeline.enable_attention_slicing()
            logger.info(f"Standard Stable Diffusion loaded on {device}")
        except Exception as e:
            logger.error(f"Failed to load Stable Diffusion: {e}")
            return None
    
    return _stable_diffusion_pipeline


def get_stable_diffusion_pipeline():
    """Get or load Stable Diffusion pipeline"""
    global _stable_diffusion_pipeline
    
    if _stable_diffusion_pipeline is None:
        load_stable_diffusion()
    
    return _stable_diffusion_pipeline


def check_ollama_running():
    """Check if Ollama service is running"""
    import httpx
    import asyncio
    
    try:
        host = os.getenv("MODEL_HOST", "http://localhost:11434")
        response = httpx.get(f"{host}/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False


async def get_available_models():
    """Get list of available models from Ollama"""
    import httpx
    
    try:
        host = os.getenv("MODEL_HOST", "http://localhost:11434")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{host}/api/tags", timeout=5.0)
        
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [m["name"] for m in models]
        else:
            return ["mistral"]  # Default fallback
    except Exception as e:
        logger.warning(f"Could not fetch Ollama models: {e}")
        return ["mistral"]  # Default fallback
