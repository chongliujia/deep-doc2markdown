import uvicorn
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.document_api import router as document_router
from app.api.static_files import router as static_router
from app.frontend.frontend_api import router as frontend_router
from config.config import HOST, PORT, DEBUG, MEDIA_DIR

# Create the FastAPI app
app = FastAPI(
    title="Document to Markdown Converter",
    description="Convert PDF, Word documents, and images to Markdown",
    version="1.0.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# Include routers
app.include_router(document_router, prefix="/api", tags=["Document API"])
app.include_router(static_router, prefix="/media", tags=["Static Files"])
app.include_router(frontend_router, tags=["Frontend"])


if __name__ == "__main__":
    # Create necessary directories
    os.makedirs(MEDIA_DIR, exist_ok=True)
    
    # Run the application
    uvicorn.run("main:app", host=HOST, port=PORT, reload=DEBUG) 