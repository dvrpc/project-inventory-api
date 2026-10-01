from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AttachmentResponse(BaseModel):
    attachment_id: int
    pub_id: Optional[int]
    file_name: str
    mime_type: Optional[str]
    file_size: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AttachmentCreateRequest(BaseModel):
    pub_id: Optional[int] = None
    file_name: str
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    file_content: Optional[bytes] = None

class AttachmentUpdateRequest(BaseModel):
    pub_id: Optional[int] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    file_content: Optional[bytes] = None
