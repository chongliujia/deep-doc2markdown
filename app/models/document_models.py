from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
import datetime


class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    IMAGE = "image"


class DocumentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ImageInfo(BaseModel):
    filename: str
    path: str
    width: Optional[int] = None
    height: Optional[int] = None
    page: Optional[int] = None
    index: Optional[int] = None
    ocr_text: Optional[str] = None
    markdown: Optional[str] = None


class TextItem(BaseModel):
    content: str
    type: Optional[str] = "paragraph"
    page: Optional[int] = None
    index: Optional[int] = None
    style: Optional[str] = None


class OCRResult(BaseModel):
    full_text: Optional[str] = None
    details: Optional[List[Dict[str, Any]]] = None


class DocumentData(BaseModel):
    doc_id: str
    filename: str
    original_path: str
    doc_type: DocumentType
    text: Optional[List[TextItem]] = None
    images: Optional[List[ImageInfo]] = None
    ocr: Optional[OCRResult] = None
    merged_text: Optional[List[Any]] = None
    markdown: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    status: DocumentStatus = DocumentStatus.PENDING
    error: Optional[str] = None


class DocumentRequest(BaseModel):
    filename: str
    doc_type: DocumentType


class DocumentResponse(BaseModel):
    doc_id: str
    filename: str
    doc_type: DocumentType
    status: DocumentStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    markdown: Optional[str] = None
    error: Optional[str] = None 