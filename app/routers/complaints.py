from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import ComplaintCreate, Complaint, ComplaintUpdate, UserInDB
from app.crud import create_complaint, get_complaint, update_complaint, delete_complaint, get_complaints_by_user
from app.auth import get_current_user
from app.database import get_db

router = APIRouter(
    prefix="/complaints",
    tags=["complaints"],
    responses={404: {"description": "Complaint not found"}},
)

@router.post("/", response_model=Complaint, status_code=status.HTTP_201_CREATED)
def create_complaintt(complaint: ComplaintCreate, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    return create_complaint(db=db, complaint=complaint, user_id=current_user.id)

@router.get("/{complaint_id}", response_model=Complaint)
def get_complaint_by_id(complaint_id: int, db: Session = Depends(get_db)):
    db_complaint = get_complaint(db, complaint_id=complaint_id)
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return db_complaint

@router.get("/", response_model=list[Complaint])
def get_complaints_by_userr(db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    return get_complaints_by_user(db=db, user_id=current_user.id)

@router.put("/{complaint_id}", response_model=Complaint)
def update_complaint_by_id(complaint_id: int, complaint: ComplaintUpdate, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    db_complaint = get_complaint(db, complaint_id=complaint_id)
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    if db_complaint.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to edit this complaint")
    return update_complaint(db=db, db_complaint=db_complaint, complaint=complaint)

@router.delete("/{complaint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_complaint_by_id(complaint_id: int, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    db_complaint = get_complaint(db, complaint_id=complaint_id)
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    if db_complaint.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this complaint")
    delete_complaint(db=db, db_complaint=db_complaint)