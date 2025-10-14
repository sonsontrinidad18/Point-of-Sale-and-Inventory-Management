from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import CheckoutRequest
from services import checkout, sales_summary
from security import require_role
from fastapi.responses import StreamingResponse
import io, csv

router = APIRouter(prefix="/api", tags=["sales"])

@router.post("/checkout")
def post_checkout(payload: CheckoutRequest, db: Session = Depends(get_db), user = Depends(require_role("associate","manager","admin"))):
    sale = checkout(db, payload)
    return {"id": sale.id, "total": sale.total}

@router.get("/report/sales")
def report_sales(store_id:int, date_from:str|None=None, date_to:str|None=None, db: Session = Depends(get_db), user = Depends(require_role("manager","admin"))):
    return sales_summary(db, store_id, date_from, date_to)

@router.get("/export/inventory.csv")
def export_inventory_csv(store_id:int, db: Session = Depends(get_db), user = Depends(require_role("manager","admin"))):
    from services import list_inventory
    rows = list_inventory(db, store_id)
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=["product_id","sku","name","price","qty"])
    w.writeheader(); w.writerows(rows)
    mem = io.BytesIO(out.getvalue().encode("utf-8"))
    return StreamingResponse(mem, media_type="text/csv", headers={"Content-Disposition":"attachment; filename=inventory.csv"})
