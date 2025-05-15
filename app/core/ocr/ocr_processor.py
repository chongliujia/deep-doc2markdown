from app.core.ocr.paddle_ocr import PaddleOCRProcessor


class OCRProcessor:
    def __init__(self):
        self.ocr_engine = PaddleOCRProcessor()
    
    def process_single_image(self, image_path):
        """
        Process a single image with OCR.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            OCR results
        """
        return self.ocr_engine.process_image(image_path)
    
    def process_multiple_images(self, image_paths):
        """
        Process multiple images with OCR and combine results.
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            Combined OCR results
        """
        return self.ocr_engine.process_images(image_paths)
    
    def process_document_images(self, document_data):
        """
        Process all images extracted from a document.
        
        Args:
            document_data: Dictionary containing extracted document data with images
            
        Returns:
            Updated document data with OCR results for each image
        """
        # Make a copy of the input data to avoid modifying the original
        result = document_data.copy()
        
        # If there are no images, return the original data
        if "images" not in result or not result["images"]:
            return result
        
        # Get paths of all images
        image_paths = [img["path"] for img in result["images"]]
        
        # Process all images as a batch
        ocr_results = self.process_multiple_images(image_paths)
        
        # Add OCR results to each image
        for i, img in enumerate(result["images"]):
            # Find OCR details for this image
            img_details = [detail for detail in ocr_results["details"] 
                          if detail.get("image_index") == i]
            
            # Add OCR text to the image
            img["ocr_text"] = " ".join([detail["text"] for detail in img_details])
            img["ocr_details"] = img_details
        
        # Add combined OCR text to the document
        if "ocr" not in result:
            result["ocr"] = {}
        
        result["ocr"]["full_text"] = ocr_results["text"]
        result["ocr"]["details"] = ocr_results["details"]
        
        return result 