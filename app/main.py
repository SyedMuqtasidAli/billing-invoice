from fastapi import FastAPI
from app import models, database, routes

app = FastAPI(title="Invoice Billing System")

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)

app.include_router(routes.router)
