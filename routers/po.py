from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import POIn
from services import create_po, receive_po
from security import require_role

router = APIRouter(prefix="/api/po", tags=["purchase_orders"])

@router.post("/create")
def create(data: POIn, db: Session = Depends(get_db), user = Depends(require_role("buyer","manager","admin"))):
    po_id = create_po(db, data)
    return {"po_id": po_id, "status": "approved"}

@router.post("/receive/{po_id}")
def receive(po_id:int, db: Session = Depends(get_db), user = Depends(require_role("manager","admin"))):
    receive_po(db, po_id)
    return {"po_id": po_id, "status": "received"}
