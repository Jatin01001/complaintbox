from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import users, complaints
from app.config import settings

# ... other imports

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(complaints.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Complaint Management System"}