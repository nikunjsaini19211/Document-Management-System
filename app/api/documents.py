from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.document import DocumentResponse, DocumentUpdate
from app.services.document import DocumentService
from app.core.security import get_current_user

# No prefix here; it's applied in main.py
router = APIRouter(tags=["documents"])

@router.post("/", response_model=DocumentResponse)
async def create_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    file_type: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Authorization: only admins and editors
    if current_user.role not in [UserRole.ADMIN, UserRole.EDITOR]:
        raise HTTPException(status_code=403, detail="Not authorized to create documents")

    document_service = DocumentService(db)
    return await document_service.create_document(
        title=title,
        description=description,
        file_type=file_type,
        file=file,
        owner_id=current_user.id
    )

@router.get("/", response_model=List[DocumentResponse])
def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document_service = DocumentService(db)
    return document_service.get_documents(skip=skip, limit=limit)

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document_service = DocumentService(db)
    document = document_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: int,
    request: Request,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    file_type: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Authorization: only admins and editors
    if current_user.role not in [UserRole.ADMIN, UserRole.EDITOR]:
        raise HTTPException(status_code=403, detail="Not authorized to update documents")

    document_service = DocumentService(db)
    
    # Check content type
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        # Handle JSON data
        json_data = await request.json()
        update_data = DocumentUpdate(**json_data)
        document = document_service.update_document(
            document_id,
            title=update_data.title,
            description=update_data.description,
            file_type=update_data.file_type,
            file=None
        )
    else:
        # Handle form data
        document = document_service.update_document(
            document_id,
            title=title,
            description=description,
            file_type=file_type,
            file=file
        )
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to delete documents")

    document_service = DocumentService(db)
    success = document_service.delete_document(document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}
