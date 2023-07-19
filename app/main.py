import os

from fastapi import FastAPI
from dotenv import load_dotenv

from app.services.db_service import DatabaseService
from app.routers import insurance_router


env = os.environ.get
load_dotenv('./.env')
DEBUG = (env('DEBUG').lower()=="true")
POSTGRE_CON = f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}" \
              f"@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}"

tags_metadata = [
    {
        "name": "Insurance Rates",
        "description": "CRUD operations with **insurance**",
    },
]

app = FastAPI(
    title="Insurance Rates API",
    summary="Tiny API service to get the rate of transported products 😼",
    contact={
        "name": "Segfaul",
        "url": "https://github.com/segfaul",
    },
    openapi_tags=tags_metadata
)

db_service = DatabaseService(DEBUG, POSTGRE_CON)


app.include_router(insurance_router.router)


@app.on_event("startup")
async def startup() -> None:
    await db_service.init_db()


@app.on_event("shutdown")
async def shutdown() -> None:
    await db_service.close_db()
