from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     password_hash = Column(String, nullable=False)
#     is_verified = Column(Boolean, default=False)
#     role = Column(Enum('student', 'hod', 'fr', 'rector', 'superadmin', name='user_roles'), nullable=False)

#     complaints = relationship("Complaint", backref="user")

class Hostel(Base):
    __tablename__ = "hostels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(Enum('Hostel', 'Academic', name='complaint_categories'), nullable=False)
    subcategory = Column(String, nullable=False)
    hostel_id = Column(Integer, ForeignKey("hostels.id"), nullable=True) # Optional for day scholars
    room_number = Column(String, nullable=True) # Optional for day scholars
    
    
    
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum('student', 'hod', 'fr', 'rector', 'superadmin', name='user_roles'), nullable=False)
    department = Column(String, nullable=False) # Add department field
    class_number = Column(String, nullable=False) # Add class number field
    type = Column(Enum('day_scholar', 'hosteler', name='type_of_student'), nullable=False) # Add type field
    hostel_id = Column(Integer, ForeignKey("hostels.id"), nullable=True) # Add hostel_id
    room_number = Column(String, nullable=True) # Add room number field

    complaints = relationship("Complaint", backref="user")