from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.routes import api_routes, page_routes

app = FastAPI(title="Support CRM")

app.mount("/static", StaticFiles(directory="static"), name="static")

init_db()

app.include_router(page_routes.router)
app.include_router(api_routes.router)
