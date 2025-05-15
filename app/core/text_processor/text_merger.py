class TextMerger:
    def __init__(self):
        pass
    
    def merge_document_and_ocr(self, document_data):
        """
        Merge document text and OCR text for a more complete representation.
        
        This function combines extracted document text with OCR text,
        prioritizing document text but filling in gaps with OCR where needed.
        
        Args:
            document_data: Dictionary containing document data with text and OCR results
            
        Returns:
            Updated document data with merged text
        """
        # Make a copy of the input data to avoid modifying the original
        result = document_data.copy()
        
        # If there's no OCR data, return the original document
        if "ocr" not in result or not result["ocr"]:
            return result
        
        # Add a merged_text field to the result
        result["merged_text"] = []
        
        # If the text is a list (like in DOCX with structured paragraphs)
        if "text" in result and isinstance(result["text"], list):
            # We'll preserve the structure and just add OCR text for images
            result["merged_text"] = result["text"].copy()
            
            # Add OCR text for images
            if "images" in result and result["images"]:
                for img in result["images"]:
                    if "ocr_text" in img and img["ocr_text"]:
                        # Create an entry for the image OCR text
                        result["merged_text"].append({
                            "type": "image_ocr",
                            "content": img["ocr_text"],
                            "image_info": {
                                "filename": img.get("filename", ""),
                                "path": img.get("path", "")
                            }
                        })
        
        # If the text is in a page-by-page format (like in PDF)
        elif "text" in result and isinstance(result["text"], list) and all("page" in item for item in result["text"]):
            # Organize images by page
            page_images = {}
            if "images" in result and result["images"]:
                for img in result["images"]:
                    page = img.get("page", 1)
                    if page not in page_images:
                        page_images[page] = []
                    page_images[page].append(img)
            
            # Merge text and OCR by page
            for text_item in result["text"]:
                page = text_item.get("page", 1)
                merged_item = text_item.copy()
                
                # Add OCR text for images on this page
                if page in page_images:
                    ocr_texts = []
                    for img in page_images[page]:
                        if "ocr_text" in img and img["ocr_text"]:
                            ocr_texts.append(img["ocr_text"])
                    
                    if ocr_texts:
                        merged_item["ocr_text"] = "\n\n".join(ocr_texts)
                
                result["merged_text"].append(merged_item)
        
        # If there's no structured text but there is OCR text
        elif ("text" not in result or not result["text"]) and "ocr" in result and "full_text" in result["ocr"]:
            # Just use the OCR text
            result["merged_text"] = [{
                "type": "ocr_text",
                "content": result["ocr"]["full_text"]
            }]
        
        # Default case - just copy the text
        elif "text" in result:
            result["merged_text"] = result["text"]
        
        return result 