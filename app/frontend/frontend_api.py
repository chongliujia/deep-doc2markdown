from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import os
from pathlib import Path

# Get the directory of this file
current_dir = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    """
    Serve the main application page.
    
    Parameters:
    - request: The request object
    
    Returns:
    - HTML response
    """
    return templates.TemplateResponse("index.html", {"request": request}) 