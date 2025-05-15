from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IngestionBase(BaseModel):
    document_id: int
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

class IngestionResponse(IngestionBase):
    id: int

    class Config:
        from_attributes = True 