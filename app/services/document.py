import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.document import Document
from app.core.config import settings
from app.schemas.document import DocumentUpdate

class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.upload_dir = "uploads"

    async def create_document(
        self,
        title: str,
        description: str,
        file_type: str,
        file: UploadFile,
        owner_id: int
    ) -> Document:
        os.makedirs(self.upload_dir, exist_ok=True)
        file_path = os.path.join(self.upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        document = Document(
            title=title,
            description=description,
            file_path=file_path,
            file_type=file_type,
            owner_id=owner_id
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_documents(self, skip: int = 0, limit: int = 100):
        return self.db.query(Document).offset(skip).limit(limit).all()

    def get_document(self, document_id: int):
        return self.db.query(Document).filter(Document.id == document_id).first()

    def update_document(self, document_id: int, title=None, description=None, file_type=None, file=None) -> Document:
        document = self.get_document(document_id)
        if not document:
            return None

        # Update only the fields that are explicitly provided (not None)
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if file_type is not None:
            update_data['file_type'] = file_type
        if file is not None:
            os.makedirs(self.upload_dir, exist_ok=True)
            file_path = os.path.join(self.upload_dir, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())
            update_data['file_path'] = file_path

        # Apply updates
        for field, value in update_data.items():
            setattr(document, field, value)

        self.db.commit()
        self.db.refresh(document)
        return document

    def delete_document(self, document_id: int):
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return False
        
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        self.db.delete(document)
        self.db.commit()
        return True 