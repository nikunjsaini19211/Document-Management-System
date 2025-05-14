from sqlalchemy.orm import Session
from app.models.document import Document
import asyncio

class IngestionService:
    def __init__(self, db: Session):
        self.db = db
        self.is_processing = False

    async def start_ingestion(self):
        if self.is_processing:
            return
        
        self.is_processing = True
        try:
            # Implement your document processing logic here
            documents = self.db.query(Document).all()
            for document in documents:
                # Process each document
                await self.process_document(document)
        finally:
            self.is_processing = False

    async def process_document(self, document: Document):
        # Implement document processing logic
        await asyncio.sleep(1)  # Simulate processing time

    def get_status(self):
        return {
            "is_processing": self.is_processing,
            "status": "processing" if self.is_processing else "idle"
        } 