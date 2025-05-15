from app.core.markdown_converter.structure_parser import StructureParser
from app.core.markdown_converter.image_formatter import ImageFormatter


class MarkdownFormatter:
    def __init__(self):
        self.structure_parser = StructureParser()
        self.image_formatter = ImageFormatter()
    
    def format_text_as_markdown(self, text):
        """
        Format plain text as Markdown, detecting structure and applying markup.
        
        Args:
            text: Plain text content
            
        Returns:
            Markdown-formatted text
        """
        if not text:
            return ""
        
        # 清理文本，处理换行问题
        text = self._clean_text(text)
        
        # Parse the structure of the text
        structure = self.structure_parser.parse_structure(text)
        
        # Apply Markdown formatting based on the detected structure
        md_text = text
        
        # Keep track of replacements to make
        replacements = []
        
        # Format headings
        for heading in structure["headings"]:
            level = heading["level"]
            text = heading["text"]
            start = heading["start"]
            end = heading["end"]
            
            # Create Markdown heading
            md_heading = f"{'#' * level} {text}"
            
            # Add to replacements
            replacements.append((start, end, md_heading))
        
        # Format lists
        for item in structure["lists"]:
            level = item["level"]
            text = item["text"]
            start = item["start"]
            end = item["end"]
            indent = "  " * (level - 1)
            
            if item["type"] == "bullet":
                # Create Markdown bullet list item
                md_item = f"{indent}- {text}"
            else:  # numbered
                number = item["number"]
                # Create Markdown numbered list item
                md_item = f"{indent}{number}. {text}"
            
            # Add to replacements
            replacements.append((start, end, md_item))
        
        # Format tables
        for table in structure["tables"]:
            start = table["start"]
            end = table["end"]
            rows = table["rows"]
            
            # Create Markdown table
            md_table = []
            
            # First row is the header
            if rows:
                header = rows[0]
                md_table.append("| " + " | ".join(header) + " |")
                
                # Add separator row
                separator = ["---"] * len(header)
                md_table.append("| " + " | ".join(separator) + " |")
                
                # Add data rows
                for row in rows[1:]:
                    md_table.append("| " + " | ".join(row) + " |")
            
            # Join the table rows
            md_table_text = "\n".join(md_table)
            
            # Add to replacements
            replacements.append((start, end, md_table_text))
        
        # Sort replacements from end to start to avoid position shifts
        replacements.sort(reverse=True, key=lambda x: x[0])
        
        # Apply replacements
        for start, end, replacement in replacements:
            md_text = md_text[:start] + replacement + md_text[end:]
        
        return md_text
    
    def _clean_text(self, text):
        """
        Clean text for better Markdown formatting
        """
        # 替换多个连续换行为两个换行 (保留段落格式)
        import re
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 确保段落之间有适当的空行
        text = re.sub(r'([^\n])\n([^\n])', r'\1\n\n\2', text)
        
        return text
    
    def format_document_as_markdown(self, document_data):
        """
        Convert document data to Markdown format.
        
        Args:
            document_data: Dictionary containing document data
            
        Returns:
            Markdown-formatted text
        """
        # Format images for Markdown
        doc_with_images = self.image_formatter.format_document_images(document_data)
        
        # Initialize Markdown content
        markdown_content = ""
        
        # Add document title if available
        if "title" in doc_with_images and doc_with_images["title"]:
            markdown_content += f"# {doc_with_images['title']}\n\n"
        
        # Process based on the document structure
        if "merged_text" in doc_with_images and doc_with_images["merged_text"]:
            # If we have merged text (combined from document and OCR)
            for item in doc_with_images["merged_text"]:
                if isinstance(item, dict):
                    item_type = item.get("type", "")
                    content = item.get("content", "")
                    
                    # Format content based on type
                    if item_type == "paragraph":
                        style = item.get("style", "").lower()
                        
                        # Check if it's a heading
                        if "heading" in style or "title" in style:
                            level = 1
                            if "1" in style: level = 1
                            elif "2" in style: level = 2
                            elif "3" in style: level = 3
                            elif "4" in style: level = 4
                            elif "5" in style: level = 5
                            elif "6" in style: level = 6
                            
                            markdown_content += f"{'#' * level} {content}\n\n"
                        else:
                            # Regular paragraph
                            markdown_content += f"{content}\n\n"
                    
                    elif item_type == "table":
                        # Format table
                        table_content = item.get("content", [])
                        if table_content and isinstance(table_content, list):
                            # Create Markdown table
                            table_md = []
                            for i, row in enumerate(table_content):
                                table_md.append("| " + " | ".join(row) + " |")
                                
                                # Add separator after first row
                                if i == 0:
                                    separator = ["---"] * len(row)
                                    table_md.append("| " + " | ".join(separator) + " |")
                            
                            markdown_content += "\n".join(table_md) + "\n\n"
                    
                    elif item_type == "image_ocr":
                        # Add image with OCR text
                        image_info = item.get("image_info", {})
                        if image_info:
                            for img in doc_with_images["images"]:
                                if img.get("filename") == image_info.get("filename"):
                                    # 添加更大的间距以及分隔线
                                    markdown_content += "\n---\n\n"
                                    markdown_content += img.get("markdown", "") + "\n\n"
                                    if content.strip():
                                        markdown_content += f"*Image text:* {content}\n\n"
                                    break
                    
                    elif item_type == "ocr_text":
                        # Format OCR text
                        markdown_content += self.format_text_as_markdown(content) + "\n\n"
                    
                    else:
                        # Default case - just add the content
                        markdown_content += content + "\n\n"
                
                elif isinstance(item, str):
                    # Simple string content - 尝试检测是否应为标题
                    if len(item.strip()) < 100 and item.strip().isupper():
                        markdown_content += f"## {item}\n\n"
                    else:
                        markdown_content += self._clean_text(item) + "\n\n"
        
        # If we have text but no merged_text
        elif "text" in doc_with_images and doc_with_images["text"]:
            if isinstance(doc_with_images["text"], list):
                for item in doc_with_images["text"]:
                    if isinstance(item, dict) and "content" in item:
                        markdown_content += self.format_text_as_markdown(item["content"]) + "\n\n"
                    elif isinstance(item, str):
                        markdown_content += self.format_text_as_markdown(item) + "\n\n"
            elif isinstance(doc_with_images["text"], str):
                markdown_content += self.format_text_as_markdown(doc_with_images["text"]) + "\n\n"
        
        # Add images that weren't included in the text
        if "images" in doc_with_images and doc_with_images["images"]:
            image_section = "\n## 图片与扫描内容\n\n"
            has_images = False
            
            for img in doc_with_images["images"]:
                if "markdown" in img and img["markdown"]:
                    # Check if this image is already in the markdown_content
                    if img["markdown"] not in markdown_content:
                        # 添加分隔线以更好地区分图片
                        image_section += "---\n\n"
                        image_section += img["markdown"] + "\n\n"
                        has_images = True
                        
                        # Add OCR text if available, 使用更好的格式
                        if "ocr_text" in img and img["ocr_text"]:
                            image_section += f"*Image text:* {img['ocr_text']}\n\n"
            
            if has_images:
                markdown_content += image_section
        
        # 处理一些额外的格式问题
        markdown_content = self._format_special_elements(markdown_content)
        
        return markdown_content.strip()
        
    def _format_special_elements(self, content):
        """
        对特殊元素进行格式化处理
        """
        import re
        
        # 处理可能的边距问题
        content = re.sub(r'\n{4,}', '\n\n', content)
        
        # 确保代码块周围有适当的空白
        content = re.sub(r'```(.*?)```', r'\n\n```\1```\n\n', content, flags=re.DOTALL)
        
        # 确保标题前有足够空白
        content = re.sub(r'([^\n])(\n#{1,6} )', r'\1\n\n\2', content)
        
        return content 