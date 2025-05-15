from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from typing import Optional
import os
import uuid
import tempfile
import shutil
from datetime import datetime

from app.models.document_models import DocumentResponse, DocumentType, DocumentStatus, DocumentData
from app.core.document_extractor.pdf_extractor import PDFExtractor
from app.core.document_extractor.docx_extractor import DocxExtractor
from app.core.document_extractor.image_handler import ImageHandler
from app.core.ocr.ocr_processor import OCRProcessor
from app.core.text_processor.text_cleaner import TextCleaner
from app.core.text_processor.text_merger import TextMerger
from app.core.markdown_converter.md_formatter import MarkdownFormatter

from config.config import MEDIA_DIR

# In-memory storage for document data (replace with a database in production)
documents = {}

router = APIRouter()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    doc_type: Optional[str] = Form(None)
):
    """
    Upload a document (PDF, DOCX, or image) and convert it to Markdown.
    
    Parameters:
    - file: The file to upload
    - doc_type: The document type (pdf, docx, image). If not provided, it will be inferred from the file extension.
    
    Returns:
    - DocumentResponse with the document ID and status
    """
    # Generate a unique ID for this document
    doc_id = str(uuid.uuid4())
    
    # Get the original filename
    filename = file.filename
    
    # Determine document type if not provided
    if not doc_type:
        if filename.lower().endswith('.pdf'):
            doc_type = DocumentType.PDF
        elif filename.lower().endswith(('.docx', '.doc')):
            doc_type = DocumentType.DOCX
        elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
            doc_type = DocumentType.IMAGE
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF, DOCX, or image file.")
    else:
        doc_type = DocumentType(doc_type.lower())
    
    # Create a temporary file to store the uploaded content
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    
    try:
        # Write the uploaded file content to the temporary file
        contents = await file.read()
        with open(temp_file.name, "wb") as f:
            f.write(contents)
        
        # Create initial document data
        document_data = DocumentData(
            doc_id=doc_id,
            filename=filename,
            original_path=temp_file.name,
            doc_type=doc_type,
            status=DocumentStatus.PENDING
        )
        
        # Store the document data
        documents[doc_id] = document_data
        
        # Process the document in the background
        background_tasks.add_task(process_document, doc_id)
        
        # Return the initial response
        return DocumentResponse(
            doc_id=doc_id,
            filename=filename,
            doc_type=doc_type,
            status=DocumentStatus.PENDING,
            created_at=document_data.created_at,
            updated_at=document_data.updated_at
        )
    
    except Exception as e:
        # Clean up the temporary file
        os.unlink(temp_file.name)
        
        # Handle the error
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.get("/status/{doc_id}", response_model=DocumentResponse)
async def get_document_status(doc_id: str):
    """
    Get the status of a document processing job.
    
    Parameters:
    - doc_id: The document ID
    
    Returns:
    - DocumentResponse with the current status
    """
    if doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc_data = documents[doc_id]
    
    return DocumentResponse(
        doc_id=doc_id,
        filename=doc_data.filename,
        doc_type=doc_data.doc_type,
        status=doc_data.status,
        created_at=doc_data.created_at,
        updated_at=doc_data.updated_at,
        markdown=doc_data.markdown,
        error=doc_data.error
    )


@router.get("/markdown/{doc_id}")
async def get_document_markdown(doc_id: str):
    """
    Get the Markdown content of a processed document.
    
    Parameters:
    - doc_id: The document ID
    
    Returns:
    - Markdown content as plain text
    """
    if doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc_data = documents[doc_id]
    
    if doc_data.status != DocumentStatus.COMPLETED:
        raise HTTPException(status_code=400, detail=f"Document processing is not complete. Current status: {doc_data.status}")
    
    if not doc_data.markdown:
        raise HTTPException(status_code=404, detail="Markdown content not found")
    
    return doc_data.markdown


def process_document(doc_id: str):
    """
    Process a document in the background.
    
    Parameters:
    - doc_id: The document ID
    """
    if doc_id not in documents:
        return
    
    doc_data = documents[doc_id]
    
    try:
        # Update status to processing
        doc_data.status = DocumentStatus.PROCESSING
        doc_data.updated_at = datetime.now()
        
        # Extract content based on document type
        if doc_data.doc_type == DocumentType.PDF:
            # Process PDF
            extractor = PDFExtractor(doc_data.original_path)
            extracted_data = extractor.extract_all()
        elif doc_data.doc_type == DocumentType.DOCX:
            # Process DOCX
            extractor = DocxExtractor(doc_data.original_path)
            extracted_data = extractor.extract_all()
        elif doc_data.doc_type == DocumentType.IMAGE:
            # Process image
            handler = ImageHandler(file_path=doc_data.original_path)
            image_info = handler.process_image()
            
            # Create a structure similar to document extraction
            extracted_data = {
                "text": [],
                "images": [image_info]
            }
        else:
            raise ValueError(f"Unsupported document type: {doc_data.doc_type}")
        
        # Process OCR for images
        ocr_processor = OCRProcessor()
        ocr_data = ocr_processor.process_document_images(extracted_data)
        
        # Clean the text
        text_cleaner = TextCleaner()
        cleaned_data = text_cleaner.clean_document_text(ocr_data)
        
        # Merge document text and OCR text
        text_merger = TextMerger()
        merged_data = text_merger.merge_document_and_ocr(cleaned_data)
        
        # Convert to Markdown
        md_formatter = MarkdownFormatter()
        markdown = md_formatter.format_document_as_markdown(merged_data)
        
        # Update document data
        doc_data.text = merged_data.get("text", [])
        doc_data.images = merged_data.get("images", [])
        doc_data.ocr = merged_data.get("ocr")
        doc_data.merged_text = merged_data.get("merged_text", [])
        doc_data.markdown = markdown
        doc_data.status = DocumentStatus.COMPLETED
        doc_data.updated_at = datetime.now()
        
    except Exception as e:
        # Update status to failed
        doc_data.status = DocumentStatus.FAILED
        doc_data.error = str(e)
        doc_data.updated_at = datetime.now()
    
    finally:
        # Clean up the temporary file
        if os.path.exists(doc_data.original_path):
            os.unlink(doc_data.original_path) 