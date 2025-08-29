from fastapi import FastAPI
from . import models, database, routes

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Invoice Billing System")
app.include_router(routes.router)
