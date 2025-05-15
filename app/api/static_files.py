from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

from config.config import IMAGES_DIR

router = APIRouter()


@router.get("/images/{filename}")
async def get_image(filename: str):
    """
    Serve a static image file.
    
    Parameters:
    - filename: The image filename
    
    Returns:
    - The image file
    """
    image_path = os.path.join(IMAGES_DIR, filename)
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path) 