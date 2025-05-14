from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User, UserRole
from app.services.ingestion import IngestionService
from app.core.security import get_current_user

router = APIRouter()

@router.post("/trigger")
async def trigger_ingestion(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.EDITOR]:
        raise HTTPException(status_code=403, detail="Not authorized to trigger ingestion")
    
    ingestion_service = IngestionService(db)
    background_tasks.add_task(ingestion_service.start_ingestion)
    return {"message": "Ingestion process started"}

@router.get("/status")
async def get_ingestion_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.EDITOR]:
        raise HTTPException(status_code=403, detail="Not authorized to view ingestion status")
    
    ingestion_service = IngestionService(db)
    return ingestion_service.get_status() 