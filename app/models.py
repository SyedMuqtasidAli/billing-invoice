# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)   # subtotal before tax/discount
    tax_rate = Column(Float, default=15.0)         # percentage
    adv_tax = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    net_amount = Column(Float, nullable=False)     # final after tax/discount

    items = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"))
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    invoice = relationship("Invoice", back_populates="items")
