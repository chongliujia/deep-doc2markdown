import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = os.path.join(BASE_DIR, "app", "media")
IMAGES_DIR = os.path.join(MEDIA_DIR, "images")

# Create directories if they don't exist
os.makedirs(IMAGES_DIR, exist_ok=True)

# OCR settings
OCR_LANGUAGE = "ch"  # Default language for OCR
OCR_USE_ANGLE_CLS = True
OCR_USE_GPU = False

# Web settings
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true" 