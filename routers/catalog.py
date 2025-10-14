from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import list_stores, list_inventory
from schemas import StoreOut, InventoryOut
from security import require_user

router = APIRouter(prefix="/api", tags=["catalog"])

@router.get("/stores", response_model=list[StoreOut])
def get_stores(db: Session = Depends(get_db), user = Depends(require_user)):
    return list_stores(db)

@router.get("/inventory", response_model=list[InventoryOut])
def get_inventory(store_id:int, db: Session = Depends(get_db), user = Depends(require_user)):
    return list_inventory(db, store_id)
