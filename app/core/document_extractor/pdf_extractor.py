import os
import uuid
from PyPDF2 import PdfReader
from PIL import Image
import io

from config.config import IMAGES_DIR


class PDFExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text_content = []
        self.images = []
        self.structure = {}

    def extract_text(self):
        """Extract text from PDF file."""
        reader = PdfReader(self.file_path)
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                self.text_content.append({
                    "page": i + 1,
                    "content": page_text
                })
        return self.text_content

    def extract_images(self):
        """Extract images from PDF file using PyPDF2."""
        reader = PdfReader(self.file_path)
        
        for page_index, page in enumerate(reader.pages):
            img_index = 0
            for img_index, image in enumerate(page.images):
                try:
                    # Extract image data
                    image_bytes = image.data
                    
                    # Generate a unique filename
                    image_filename = f"pdf_image_{uuid.uuid4()}.png"
                    image_path = os.path.join(IMAGES_DIR, image_filename)
                    
                    # Save the image
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    # Create PIL image to get dimensions
                    pil_image = Image.open(io.BytesIO(image_bytes))
                    width, height = pil_image.size
                    
                    # Store image metadata
                    self.images.append({
                        "page": page_index + 1,
                        "index": img_index,
                        "filename": image_filename,
                        "path": image_path,
                        "width": width,
                        "height": height
                    })
                except Exception as e:
                    print(f"Error extracting image: {e}")
        
        return self.images

    def extract_all(self):
        """Extract both text and images from PDF."""
        self.extract_text()
        self.extract_images()
        
        return {
            "text": self.text_content,
            "images": self.images
        } 