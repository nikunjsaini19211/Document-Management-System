from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.ingestion import Ingestion
import asyncio
from datetime import datetime

class IngestionService:
    def __init__(self, db: Session):
        self.db = db
        self.is_processing = False

    async def start_ingestion(self):
        if self.is_processing:
            return
        
        self.is_processing = True
        try:
            # Get all documents that haven't been ingested
            documents = self.db.query(Document).all()
            for document in documents:
                # Create ingestion log
                ingestion = Ingestion(
                    document_id=document.id,
                    status="processing",
                    started_at=datetime.utcnow()
                )
                self.db.add(ingestion)
                self.db.commit()
                
                try:
                    # Process each document
                    await self.process_document(document)
                    
                    # Update ingestion log on success
                    ingestion.status = "completed"
                    ingestion.completed_at = datetime.utcnow()
                except Exception as e:
                    # Update ingestion log on failure
                    ingestion.status = "failed"
                    ingestion.error_message = str(e)
                    ingestion.completed_at = datetime.utcnow()
                
                self.db.commit()
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

    def get_all_ingestions(self):
        return self.db.query(Ingestion).order_by(Ingestion.started_at.desc()).all() 