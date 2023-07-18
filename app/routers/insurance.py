import datetime
import json

from fastapi import APIRouter, UploadFile, HTTPException

from app.services.insurance import InsuranceService


router = APIRouter(
    prefix='/insurance',
)

insurance_service = InsuranceService()


@router.delete("/rates/delete", tags=["Insurance Rates"])
async def delete_rate(date: datetime.date = None, rate_id: int = None):

    response = await insurance_service.delete_rates(date, rate_id)

    if response:
        return {200: "Succesfully deleted Insurance rates"}

    raise HTTPException(status_code=404, detail="Rate Inusrance not found")


@router.put("/rates/change", tags=["Insurance Rates"])
async def update_rate(date: datetime.date, cargo_type: str, rate: float):
    response = await insurance_service.update_rates(date, cargo_type, rate)

    if response:
        return response
    
    raise HTTPException(status_code=404, detail="Rate Inusrance not found")


@router.post("/rates/create", tags=["Insurance Rates"])
async def create_rate(date: datetime.date, cargo_type: str, rate: float):
    response = await insurance_service.populate_db(
        {date: [{"cargo_type": cargo_type, "rate": rate}]}
    )

    if type(response) == dict:
        return {200: f"Changed {response['changed']}/{response['all']}"}
    
    else:
        raise HTTPException(status_code=400, detail="Bad Request")


@router.post("/rates/upload", tags=["Insurance Rates"])
async def upload_rates(file: UploadFile = None):
    if file.content_type not in ["application/json"]:
        raise HTTPException(status_code=400, detail="Incorrect file format (only .json provided)")
    data = file.file
    response = await insurance_service.populate_db(json.load(data))

    if type(response) == dict:
        return {200: f"Changed {response['changed']}/{response['all']}"}
    
    else:
        raise HTTPException(status_code=400, detail="Bad Request")


@router.get("/rates", tags=["Insurance Rates"])
async def rates_list(date: datetime.date = None):
    response = await insurance_service.get_rates(date)

    if response:
        return response

    raise HTTPException(status_code=404, detail="No rates found in database")


@router.get("/calculate", tags=["Insurance Rates"])
async def calculate_insurance(date: datetime.date, cargo_type: str):
    rate = await insurance_service.calculate_insurance(date, cargo_type)

    if rate:
        return rate

    raise HTTPException(status_code=404, detail="Insurance rate not found for cargo type and date")
