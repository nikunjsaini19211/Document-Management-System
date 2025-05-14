from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_type: str

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    file_type: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: int
    file_path: str
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        from_attributes = True 