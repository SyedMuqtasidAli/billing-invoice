from fastapi import FastAPI
from app import models, database, routes  # changed from relative to absolute import

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# FastAPI app
app = FastAPI(title="Invoice Billing System")

# Include routes
app.include_router(routes.router)
