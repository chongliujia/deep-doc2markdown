import re


class StructureParser:
    def __init__(self):
        # Regular expressions for detecting structure
        self.heading_pattern = re.compile(r'^(#+)\s+(.+)$', re.MULTILINE)
        self.list_item_pattern = re.compile(r'^(\s*)[-*]\s+(.+)$', re.MULTILINE)
        self.numbered_list_pattern = re.compile(r'^(\s*)(\d+)[\.\)]\s+(.+)$', re.MULTILINE)
        self.table_row_pattern = re.compile(r'^([^|\n]+\|[^|\n]+(?:\|[^|\n]+)*)$', re.MULTILINE)
        self.code_block_pattern = re.compile(r'```[a-z]*\n[\s\S]*?\n```', re.MULTILINE)
        
    def detect_headings(self, text):
        """
        Detect headings in the text based on style or patterns.
        
        Args:
            text: Text content to analyze
            
        Returns:
            List of detected headings with level and text
        """
        headings = []
        
        # Look for Markdown-style headings (# Heading)
        for match in self.heading_pattern.finditer(text):
            level = len(match.group(1))  # Number of # characters
            heading_text = match.group(2).strip()
            headings.append({
                "level": level,
                "text": heading_text,
                "start": match.start(),
                "end": match.end()
            })
        
        # If no headings found, look for possible headings based on formatting
        if not headings:
            lines = text.split('\n')
            current_line_idx = 0
            
            for i, line in enumerate(lines):
                # Skip if already past this line
                if i < current_line_idx:
                    continue
                
                line = line.strip()
                current_line_idx = i + 1
                
                # Skip empty lines
                if not line:
                    continue
                
                # Check if the line is all uppercase and not too long
                if line.isupper() and len(line) < 100:
                    level = 1 if len(line) < 50 else 2
                    headings.append({
                        "level": level,
                        "text": line,
                        "start": text.find(line),
                        "end": text.find(line) + len(line)
                    })
                
                # Check if the line is followed by underlines (===== or -----)
                elif i < len(lines) - 1:
                    next_line = lines[i + 1].strip()
                    if next_line and (all(c == '=' for c in next_line) or all(c == '-' for c in next_line)):
                        level = 1 if '=' in next_line else 2
                        headings.append({
                            "level": level,
                            "text": line,
                            "start": text.find(line),
                            "end": text.find(line) + len(line) + len(next_line) + 1
                        })
                        current_line_idx = i + 2  # Skip the underline
        
        return headings
    
    def detect_lists(self, text):
        """
        Detect bullet and numbered lists in the text.
        
        Args:
            text: Text content to analyze
            
        Returns:
            List of detected list items with type, level, and text
        """
        list_items = []
        
        # Find bullet list items
        for match in self.list_item_pattern.finditer(text):
            indent = len(match.group(1))
            level = indent // 2 + 1  # Each 2 spaces = 1 level of indentation
            item_text = match.group(2).strip()
            list_items.append({
                "type": "bullet",
                "level": level,
                "text": item_text,
                "start": match.start(),
                "end": match.end()
            })
        
        # Find numbered list items
        for match in self.numbered_list_pattern.finditer(text):
            indent = len(match.group(1))
            level = indent // 2 + 1  # Each 2 spaces = 1 level of indentation
            number = match.group(2)
            item_text = match.group(3).strip()
            list_items.append({
                "type": "numbered",
                "level": level,
                "number": number,
                "text": item_text,
                "start": match.start(),
                "end": match.end()
            })
        
        return list_items
    
    def detect_tables(self, text):
        """
        Detect tables in the text.
        
        Args:
            text: Text content to analyze
            
        Returns:
            List of detected tables with rows and cells
        """
        tables = []
        
        # Find consecutive table rows
        rows = [match.group(1) for match in self.table_row_pattern.finditer(text)]
        
        if rows:
            # Group consecutive rows into tables
            current_table = []
            current_table_start = None
            
            for i, row in enumerate(rows):
                row_start = text.find(row)
                
                # If this is the first row or it's consecutive to the previous row
                if not current_table or (row_start - (text.find(rows[i-1]) + len(rows[i-1]))) < 5:
                    if not current_table:
                        current_table_start = row_start
                    current_table.append(row)
                else:
                    # This row is not consecutive, so finalize the current table
                    if current_table:
                        tables.append(self._process_table(current_table, current_table_start))
                    
                    # Start a new table
                    current_table = [row]
                    current_table_start = row_start
            
            # Add the last table if there is one
            if current_table:
                tables.append(self._process_table(current_table, current_table_start))
        
        return tables
    
    def _process_table(self, rows, start_position):
        """
        Process a group of rows into a table structure.
        
        Args:
            rows: List of table row strings
            start_position: Starting position in the original text
            
        Returns:
            Table structure with cells
        """
        processed_rows = []
        
        for row in rows:
            cells = [cell.strip() for cell in row.split('|')]
            # Remove empty cells from the beginning and end (caused by leading/trailing |)
            if cells and not cells[0]:
                cells = cells[1:]
            if cells and not cells[-1]:
                cells = cells[:-1]
                
            processed_rows.append(cells)
        
        return {
            "rows": processed_rows,
            "start": start_position,
            "end": start_position + sum(len(row) for row in rows) + len(rows) - 1
        }
    
    def detect_code_blocks(self, text):
        """
        Detect code blocks in the text.
        
        Args:
            text: Text content to analyze
            
        Returns:
            List of detected code blocks
        """
        code_blocks = []
        
        # Find code blocks enclosed in ```
        for match in self.code_block_pattern.finditer(text):
            block = match.group(0)
            first_newline = block.find('\n')
            language = block[3:first_newline].strip()
            code = block[first_newline+1:-4].strip()
            
            code_blocks.append({
                "language": language,
                "code": code,
                "start": match.start(),
                "end": match.end()
            })
        
        return code_blocks
    
    def parse_structure(self, text):
        """
        Parse the structure of the text, identifying headings, lists, tables, etc.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary with the structure information
        """
        if not text:
            return {
                "headings": [],
                "lists": [],
                "tables": [],
                "code_blocks": []
            }
        
        structure = {
            "headings": self.detect_headings(text),
            "lists": self.detect_lists(text),
            "tables": self.detect_tables(text),
            "code_blocks": self.detect_code_blocks(text)
        }
        
        return structure 