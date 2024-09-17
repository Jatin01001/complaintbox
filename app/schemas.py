from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from enum import Enum

class UserRoles(str, Enum):
    student = 'student'
    hod = 'hod'
    fr = 'fr'
    rector = 'rector'
    superadmin = 'superadmin'

class ComplaintCategories(str, Enum):
    Hostel = 'Hostel'
    Academic = 'Academic'

class Student_type(str, Enum):
    Hostel = 'hosteler'
    day_scholar = 'day_scholar'


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str

# class UserCreate(UserBase):
#     role: UserRoles = UserRoles.student  # Use UserRoles enum

class UserUpdate(UserBase):
    password: Optional[str] = None
    role: Optional[UserRoles] = None  # Use UserRoles enum

# class UserInDB(BaseModel):
#     id: int
#     is_verified: bool
#     role: UserRoles
#     name: str
#     email: EmailStr

class UserInDB(BaseModel):
    id: int
    is_verified: bool
    role: UserRoles
    name: str
    email: EmailStr
    department: str
    class_number: str
    type: Student_type
    hostel_name: Optional[str] = None # Optional for day scholars
    room_number: Optional[str] = None # Optional for day scholars
    
    

class User(UserInDB):
    pass

class ComplaintBase(BaseModel):
    title: str
    description: str
    category: ComplaintCategories  # Use ComplaintCategories enum
    subcategory: str

class ComplaintCreate(ComplaintBase):
    hostel_id: Optional[int]
    room_number: Optional[str]

class ComplaintUpdate(ComplaintBase):
    hostel_id: Optional[int]
    room_number: Optional[str]
    category: Optional[ComplaintCategories]  # Use ComplaintCategories enum

class ComplaintInDB(ComplaintBase):
    id: int
    user_id: int
    hostel_id: Optional[int]
    room_number: Optional[str]

class Complaint(ComplaintInDB):
    user: UserInDB

class HostelBase(BaseModel):
    name: str

class HostelCreate(HostelBase):
    pass

class Hostel(HostelBase):
    id: int
    hostel_name: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
    
    
    
class UserCreate(UserBase):
    role: UserRoles = UserRoles.student  # Use UserRoles enum
    department: str 
    class_number: str
    type: Student_type # 'day scholar' or 'hosteler'
    hostel_name: Optional[str] = None # Optional for day scholars
    room_number: Optional[str] = None # Optional for day scholars

    @validator('type')
    def type_must_be_valid(cls, value):
        if value not in ['day_scholar', 'hosteler']:
            raise ValueError('Type must be either "day scholar" or "hosteler"')
        return value

    @validator('hostel_name')
    def hostel_name_required_for_hostel(cls, value, values):
        if values.get('type', None) == 'hosteler' and not value:
            raise ValueError('Hostel name is required for hostellers')
        return value

    @validator('room_number')
    def room_number_required_for_hostel(cls, value, values):
        if values.get('type', None) == 'hosteler' and not value:
            raise ValueError('Room number is required for hostellers')
        return value