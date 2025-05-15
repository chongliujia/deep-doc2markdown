# Deep Doc2Markdown

A powerful document-to-markdown converter that extracts text and images from PDF, Word documents, and images, using OCR where needed, to generate clean Markdown output.

## Features

- Extract text and images from PDF and Word documents
- Process standalone images with OCR
- Use PaddleOCR for high-quality optical character recognition
- Convert document structure to proper Markdown formatting
- Modern web interface for uploading files and viewing results
- Side-by-side view of original document and Markdown output

## Project Structure

```
document-to-markdown/
│
├── app/
│   ├── core/
│   │   ├── document_extractor/      # Extract content from documents
│   │   │   ├── pdf_extractor.py     # Extract text and images from PDF
│   │   │   ├── docx_extractor.py    # Extract text and images from Word
│   │   │   └── image_handler.py     # Process standalone images
│   │   │
│   │   ├── ocr/
│   │   │   ├── paddle_ocr.py        # PaddleOCR implementation
│   │   │   └── ocr_processor.py     # OCR processing workflow
│   │   │
│   │   ├── text_processor/          # Text processing module
│   │   │   ├── text_cleaner.py      # Text cleaning
│   │   │   └── text_merger.py       # Merge document and OCR text
│   │   │
│   │   └── markdown_converter/      # Markdown conversion module
│   │       ├── md_formatter.py      # Text to Markdown conversion
│   │       ├── image_formatter.py   # Image processing and Markdown syntax
│   │       └── structure_parser.py  # Parse document structure
│   │
│   ├── media/                       # Store processed images
│   │   └── images/                  
│   │
│   ├── api/                         # API endpoints
│   │   ├── document_api.py          # Document processing API
│   │   └── static_files.py          # Serve static files
│   │
│   ├── models/                      # Data models
│   │   └── document_models.py       # Document data models
│   │
│   └── frontend/                    # Web interface
│       ├── frontend_api.py          # Frontend API
│       └── templates/               # HTML templates
│           └── index.html           # Main app page
│
├── config/                          # Configuration
│   └── config.py                    # App configuration
│
├── requirements.txt                 # Dependencies
└── main.py                          # Main application
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/deep-doc2markdown.git
   cd deep-doc2markdown
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install PaddlePaddle:
   
   Depending on your system, you might need specific installation instructions for PaddlePaddle. Visit the [PaddlePaddle installation guide](https://www.paddlepaddle.org.cn/en/install/quick) for details.

## Usage

1. Start the application:
   ```
   python main.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

3. Use the web interface to upload your documents and convert them to Markdown.

## API Endpoints

- `POST /api/upload`: Upload a document for conversion
- `GET /api/status/{doc_id}`: Check the status of a conversion job
- `GET /api/markdown/{doc_id}`: Get the generated Markdown content

## Development

### Requirements

- Python 3.8+
- FastAPI
- PyPDF2 for PDF processing
- python-docx for Word document processing
- PaddleOCR for image text recognition
- Jinja2 for templating

### Configuration

Edit `config/config.py` to adjust settings:

- Change the server host and port
- Configure OCR settings
- Modify file storage paths

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) for the OCR functionality
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [PyPDF2](https://pythonhosted.org/PyPDF2/) for PDF processing
