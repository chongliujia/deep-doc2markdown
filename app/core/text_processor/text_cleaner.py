import re


class TextCleaner:
    def __init__(self):
        # Common patterns to clean
        self.patterns = {
            "multiple_spaces": re.compile(r'\s+'),
            "multiple_newlines": re.compile(r'\n{3,}'),
            "special_chars": re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]')
        }
    
    def clean_text(self, text):
        """
        Clean raw text by removing unwanted characters and normalizing spacing.
        
        Args:
            text: The text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove special characters
        cleaned = self.patterns["special_chars"].sub('', text)
        
        # Replace multiple spaces with a single space
        cleaned = self.patterns["multiple_spaces"].sub(' ', cleaned)
        
        # Replace more than 2 consecutive newlines with 2 newlines
        cleaned = self.patterns["multiple_newlines"].sub('\n\n', cleaned)
        
        # Strip leading/trailing whitespace
        cleaned = cleaned.strip()
        
        return cleaned
    
    def clean_ocr_text(self, ocr_text, confidence_threshold=0.7):
        """
        Clean OCR text, filtering out low-confidence text if confidence data is available.
        
        Args:
            ocr_text: Dictionary with OCR text and details
            confidence_threshold: Minimum confidence threshold for OCR results
            
        Returns:
            Cleaned OCR text
        """
        if not ocr_text:
            return ""
        
        # If we just have a string, clean it normally
        if isinstance(ocr_text, str):
            return self.clean_text(ocr_text)
        
        # If we have a dictionary with details, filter by confidence
        if isinstance(ocr_text, dict) and "details" in ocr_text:
            # Filter out low-confidence text
            high_confidence_text = []
            for detail in ocr_text["details"]:
                if detail.get("confidence", 0) >= confidence_threshold:
                    high_confidence_text.append(detail.get("text", ""))
            
            filtered_text = " ".join(high_confidence_text)
            return self.clean_text(filtered_text)
        
        # If it's a dict but doesn't have details, try to get the text
        if isinstance(ocr_text, dict) and "text" in ocr_text:
            return self.clean_text(ocr_text["text"])
        
        return ""
    
    def clean_document_text(self, document_data):
        """
        Clean the text content of a document.
        
        Args:
            document_data: Dictionary containing document data with text content
            
        Returns:
            Updated document data with cleaned text
        """
        # Make a copy of the input data to avoid modifying the original
        result = document_data.copy()
        
        # Clean main text content
        if "text" in result:
            if isinstance(result["text"], list):
                for i, text_item in enumerate(result["text"]):
                    if "content" in text_item:
                        result["text"][i]["content"] = self.clean_text(text_item["content"])
            elif isinstance(result["text"], str):
                result["text"] = self.clean_text(result["text"])
        
        # Clean OCR text if present
        if "ocr" in result and "full_text" in result["ocr"]:
            result["ocr"]["full_text"] = self.clean_ocr_text(result["ocr"])
        
        # Clean OCR text in images
        if "images" in result:
            for i, img in enumerate(result["images"]):
                if "ocr_text" in img:
                    result["images"][i]["ocr_text"] = self.clean_text(img["ocr_text"])
        
        return result 