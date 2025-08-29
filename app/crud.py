# crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def create_invoice(db: Session, invoice: schemas.InvoiceCreate) -> models.Invoice:
    subtotal = sum(item.quantity * item.unit_price for item in invoice.items)
    tax_amount = subtotal * (invoice.tax_rate / 100.0)
    net_amount = subtotal + tax_amount + invoice.adv_tax - invoice.discount

    db_invoice = models.Invoice(
        customer_name=invoice.customer_name,
        address=invoice.address,
        total_amount=subtotal,
        tax_rate=invoice.tax_rate,
        adv_tax=invoice.adv_tax,
        discount=invoice.discount,
        net_amount=net_amount,
    )
    db.add(db_invoice)
    db.flush()  # ensures db_invoice.id is available before adding items

    for item in invoice.items:
        db_item = models.InvoiceItem(
            invoice_id=db_invoice.id,
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.quantity * item.unit_price,
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_invoices(db: Session):
    return db.query(models.Invoice).all()

def get_invoice(db: Session, invoice_id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
