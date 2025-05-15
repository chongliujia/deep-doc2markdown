import os
import uuid
from PIL import Image
import io

from config.config import IMAGES_DIR


class ImageHandler:
    def __init__(self, file_path=None, file_bytes=None):
        self.file_path = file_path
        self.file_bytes = file_bytes
        self.image_info = {}
    
    def process_image(self):
        """Process an image file and save it to the images directory."""
        try:
            # Open the image, either from a file path or from bytes
            if self.file_path:
                image = Image.open(self.file_path)
                filename = os.path.basename(self.file_path)
                # Get original format extension
                ext = os.path.splitext(filename)[1].lower()
                if not ext:
                    ext = ".png"  # Default to png if no extension
            elif self.file_bytes:
                image = Image.open(io.BytesIO(self.file_bytes))
                ext = ".png"  # Default to png for bytes input
            else:
                raise ValueError("Either file_path or file_bytes must be provided")
            
            # Generate a unique filename
            unique_id = str(uuid.uuid4())
            if not ext.startswith("."):
                ext = "." + ext
            image_filename = f"uploaded_image_{unique_id}{ext}"
            image_path = os.path.join(IMAGES_DIR, image_filename)
            
            # Save the image
            image.save(image_path)
            
            # Store image metadata
            self.image_info = {
                "filename": image_filename,
                "path": image_path,
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode
            }
            
            return self.image_info
        
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")
    
    def get_relative_path(self):
        """Return the relative path to the image for use in markdown."""
        if not self.image_info:
            return None
        
        return f"/media/images/{self.image_info['filename']}" 