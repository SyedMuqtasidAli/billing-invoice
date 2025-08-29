from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from . import crud, schemas, database

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(database.get_db)):
    invoices = crud.get_invoices(db)
    return templates.TemplateResponse("invoice_list.html", {"request": request, "invoices": invoices})

@router.get("/invoice/new", response_class=HTMLResponse)
def new_invoice_form(request: Request):
    return templates.TemplateResponse("invoice_form.html", {"request": request})

# routes.py (excerpt)
@router.post("/invoice/new")
def create_invoice(
    request: Request,
    customer_name: str = Form(...),
    address: str = Form(""),
    # repeated inputs → List[...] automatically
    item_no: List[int] = Form(...),
    description: List[str] = Form(...),
    quantity: List[int] = Form(..., alias="qty"),
    unit_price: List[float] = Form(...),
    bonus: List[int] = Form(...),  # optional, ignored in DB unless you add a column
    tax_rate: float = Form(15.0),
    adv_tax: float = Form(0.0),
    discount: float = Form(0.0),
    db: Session = Depends(database.get_db),
):
    items = [
        schemas.InvoiceItemCreate(description=d, quantity=q, unit_price=u)
        for d, q, u in zip(description, quantity, unit_price)
    ]
    invoice = schemas.InvoiceCreate(
        customer_name=customer_name,
        address=address,
        tax_rate=tax_rate,
        adv_tax=adv_tax,
        discount=discount,
        items=items
    )
    crud.create_invoice(db, invoice)
    invoices = crud.get_invoices(db)
    return templates.TemplateResponse("invoice_list.html", {"request": request, "invoices": invoices})




from fastapi import HTTPException

@router.get("/invoice/{invoice_id}", response_class=HTMLResponse)
def view_invoice(invoice_id: int, request: Request, db: Session = Depends(database.get_db)):
    invoice = crud.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return templates.TemplateResponse("invoice_print.html", {"request": request, "invoice": invoice})

