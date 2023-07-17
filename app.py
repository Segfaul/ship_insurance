import os
import datetime
import json

from fastapi import FastAPI, UploadFile, HTTPException
from dotenv import load_dotenv

from database.dbapi import InsuranceRatesService


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

db_service = InsuranceRatesService(DEBUG, POSTGRE_CON)


@app.on_event("startup")
async def startup() -> None:
    await db_service.init_db()


@app.on_event("shutdown")
async def shutdown() -> None:
    await db_service.close_db()


@app.delete("/insurance/rates/delete", tags=["Insurance Rates"])
async def delete_rate(date: datetime.date = None, rate_id: int = None):

    response = await db_service.delete_rates(date, rate_id)

    if response:
        return {200: "Succesfully deleted Insurance rates"}

    raise HTTPException(status_code=404, detail="Rate Inusrance not found")


@app.put("/insurance/rates/change", tags=["Insurance Rates"])
async def update_rate(date: datetime.date, cargo_type: str, rate: float):
    response = await db_service.update_rates(date, cargo_type, rate)

    if response:
        return response
    
    raise HTTPException(status_code=404, detail="Rate Inusrance not found")


@app.post("/insurance/rates/create", tags=["Insurance Rates"])
async def create_rate(date: datetime.date, cargo_type: str, rate: float):
    response = await db_service.populate_db(
        {date: [{"cargo_type": cargo_type, "rate": rate}]}
    )

    if type(response) == dict:
        return {200: f"Changed {response['changed']}/{response['all']}"}
    
    else:
        raise HTTPException(status_code=400, detail="Bad Request")


@app.post("/insurance/rates/upload", tags=["Insurance Rates"])
async def upload_rates(file: UploadFile = None):
    if file.content_type not in ["application/json"]:
        raise HTTPException(status_code=400, detail="Incorrect file format (only .json provided)")
    data = file.file
    response = await db_service.populate_db(json.load(data))

    if type(response) == dict:
        return {200: f"Changed {response['changed']}/{response['all']}"}
    
    else:
        raise HTTPException(status_code=400, detail="Bad Request")


@app.get("/insurance/rates", tags=["Insurance Rates"])
async def rates_list(date: datetime.date = None):
    response = await db_service.get_rates(date)

    if response:
        return response

    raise HTTPException(status_code=404, detail="No rates found in database")


@app.get("/insurance/calculate", tags=["Insurance Rates"])
async def calculate_insurance(date: datetime.date, cargo_type: str):
    rate = await db_service.calculate_insurance(date, cargo_type)

    if rate:
        return rate

    raise HTTPException(status_code=404, detail="Insurance rate not found for cargo type and date")
