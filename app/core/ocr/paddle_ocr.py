from paddleocr import PaddleOCR
import os
import numpy as np
from PIL import Image

from config.config import OCR_LANGUAGE, OCR_USE_ANGLE_CLS, OCR_USE_GPU


class PaddleOCRProcessor:
    def __init__(self, lang=OCR_LANGUAGE, use_angle_cls=OCR_USE_ANGLE_CLS, use_gpu=OCR_USE_GPU):
        # Initialize PaddleOCR with specified settings
        self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, 
                            lang=lang,
                            use_gpu=use_gpu)
        
    def process_image(self, image_path):
        """
        Process an image and extract text using PaddleOCR.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with OCR results
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            # Run OCR on the image
            result = self.ocr.ocr(image_path, cls=True)
            
            # Process the results
            ocr_result = {
                "text": "",
                "details": []
            }
            
            # PaddleOCR returns a list of results, typically one per detected text region
            for line in result:
                for item in line:
                    if len(item) >= 2:
                        text = item[1][0]  # Extract the recognized text
                        confidence = item[1][1]  # Extract the confidence score
                        box = item[0]  # Coordinates of the detected text region
                        
                        # Add to the full text
                        ocr_result["text"] += text + " "
                        
                        # Add details about this text region
                        ocr_result["details"].append({
                            "text": text,
                            "confidence": confidence,
                            "box": box
                        })
            
            ocr_result["text"] = ocr_result["text"].strip()
            return ocr_result
            
        except Exception as e:
            raise Exception(f"OCR processing error: {str(e)}")
    
    def process_images(self, image_paths):
        """
        Process multiple images and combine their OCR results.
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            Dictionary with combined OCR results
        """
        combined_result = {
            "text": "",
            "details": []
        }
        
        for idx, path in enumerate(image_paths):
            try:
                result = self.process_image(path)
                combined_result["text"] += result["text"] + "\n\n"
                
                # Add image index to each detail item
                for detail in result["details"]:
                    detail["image_index"] = idx
                    combined_result["details"].append(detail)
                    
            except Exception as e:
                print(f"Error processing image {path}: {str(e)}")
                continue
        
        combined_result["text"] = combined_result["text"].strip()
        return combined_result 