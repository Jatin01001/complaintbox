from sqlalchemy.orm import Session
from app.models import User, Complaint, Hostel
from app.schemas import UserCreate, UserInDB, UserUpdate, ComplaintCreate, ComplaintUpdate, HostelCreate # Add imports for schemas
from app.auth import get_password_hash
# ... other imports


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# def create_user(db: Session, user: UserCreate):
#     # db_user = User(**user.dict())
#     user_data = user.dict(exclude={"password"})  
#     db_user = User(**user_data) 
#     db_user.password_hash = get_password_hash(user.password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, db_user: User, user: UserUpdate):
    if user.password is not None:
        db_user.password_hash = get_password_hash(user.password)
    db_user.name = user.name
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
    return f"{db_user} deleted"

# CRUD Operations for Complaint

def create_complaint(db: Session, complaint: ComplaintCreate, user_id: int):
    db_complaint = Complaint(**complaint.dict(), user_id=user_id)
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

def get_complaint(db: Session, complaint_id: int):
    return db.query(Complaint).filter(Complaint.id == complaint_id).first()

def get_complaints_by_user(db: Session, user_id: int):
    return db.query(Complaint).filter(Complaint.user_id == user_id).all()

def update_complaint(db: Session, db_complaint: Complaint, complaint: ComplaintUpdate):
    db_complaint.title = complaint.title
    db_complaint.description = complaint.description
    db_complaint.category = complaint.category
    db_complaint.subcategory = complaint.subcategory
    db_complaint.hostel_id = complaint.hostel_id
    db_complaint.room_number = complaint.room_number
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

def delete_complaint(db: Session, db_complaint: Complaint):
    db.delete(db_complaint)
    db.commit()
    




def create_user(db: Session, user: UserCreate):
    # Exclude password from the dictionary
    user_data = user.dict(exclude={"password", "hostel_name"}) 
    print("\n ====- user_data -===== ", user_data)
    # Create a new User object 
    db_user = User(**user_data)  
    db_user.password_hash = get_password_hash(user.password)
    
    # If the user is a hosteler, get hostel_id from the database
    if user.type == "hosteler":
        hostel = db.query(Hostel).filter(Hostel.name == user.hostel_name).first()
        if hostel:
            db_user.hostel_id = hostel.id 
        else:  # If hostel doesn't exist, create a new one
            new_hostel = Hostel(name=user.hostel_name)
            db.add(new_hostel)
            db.commit()
            db.refresh(new_hostel)
            db_user.hostel_id = new_hostel.id

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ... other CRUD functions for Hostel