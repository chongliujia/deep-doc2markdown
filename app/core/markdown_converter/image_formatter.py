import os
from pathlib import Path
from config.config import HOST, PORT


class ImageFormatter:
    def __init__(self, base_url="/media/images"):
        # 使用配置的主机和端口构建绝对URL基础路径
        self.server_base = f"http://{HOST}:{PORT}"
        # 保留原始的base_url作为路径
        self.base_url = base_url
        # 完整的绝对URL路径
        self.absolute_base_url = f"{self.server_base}{self.base_url}"
    
    def create_image_markdown(self, image_info, alt_text=None):
        """
        Create Markdown syntax for an image.
        
        Args:
            image_info: Dictionary with image details
            alt_text: Optional alternative text for the image
            
        Returns:
            Markdown image syntax
        """
        if not image_info:
            return ""
        
        # Get image filename
        filename = image_info.get("filename", "")
        if not filename:
            return ""
        
        # Generate image URL - 使用绝对URL
        image_url = f"{self.absolute_base_url}/{filename}"
        
        # Use OCR text as alt text if available and no alt_text provided
        if not alt_text and "ocr_text" in image_info and image_info["ocr_text"]:
            # Truncate long OCR text for alt text
            alt_text = image_info["ocr_text"][:100]
            if len(image_info["ocr_text"]) > 100:
                alt_text += "..."
        
        # Default alt text if none provided
        if not alt_text:
            alt_text = f"Image {filename}"
        
        # Create Markdown image syntax
        return f"![{alt_text}]({image_url})"
    
    def format_document_images(self, document_data):
        """
        Format all images in a document for Markdown.
        
        Args:
            document_data: Dictionary containing document data with images
            
        Returns:
            Updated document data with Markdown image references
        """
        # Make a copy of the input data to avoid modifying the original
        result = document_data.copy()
        
        # If there are no images, return the original data
        if "images" not in result or not result["images"]:
            return result
        
        # Add Markdown syntax for each image
        for i, img in enumerate(result["images"]):
            # Generate alt text using OCR if available
            alt_text = img.get("ocr_text", "")
            
            # Create Markdown syntax
            md_syntax = self.create_image_markdown(img, alt_text)
            
            # Add to the image data
            result["images"][i]["markdown"] = md_syntax
        
        return result
    
    def get_image_relative_path(self, image_path, base_dir=None):
        """
        Convert an absolute image path to a relative path for Markdown.
        
        Args:
            image_path: Absolute path to the image
            base_dir: Base directory for relative paths
            
        Returns:
            Relative path for use in Markdown
        """
        if not image_path:
            return ""
        
        # If it's already a URL or relative path, return as is
        if image_path.startswith(("http://", "https://", "/")):
            return image_path
        
        # Get the filename
        filename = os.path.basename(image_path)
        
        # Return the absolute URL
        return f"{self.absolute_base_url}/{filename}" 