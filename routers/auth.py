from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import LoginIn, LoginOut
from models import User
from database import get_db
from security import verify_pw, make_token

router = APIRouter(prefix="/api", tags=["auth"])

@router.post("/login", response_model=LoginOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.username==payload.username).first()
    if not u or not verify_pw(payload.password, u.password_hash):
        raise HTTPException(401, "Invalid credentials")
    token = make_token(u)
    return {"access_token": token, "role": u.role}
