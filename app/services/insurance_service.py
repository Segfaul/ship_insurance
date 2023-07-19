from datetime import datetime

from app.models.models import Rates


class InsuranceService:

    def __init__(self) -> None:
        ...

    @classmethod
    async def populate_db(cls, rates: dict = None) -> dict:
        total, changed = 0, 0
        data = rates

        for date, rates in data.items():
            current_rates = await Rates.filter(date=date).values("cargo_type")

            for rate in rates:
                rate['rate'] = float(rate['rate'])
                rate['cargo_type'] = rate['cargo_type'].capitalize()

                if {'cargo_type': rate['cargo_type']} not in current_rates:
                    changed += 1
                    await Rates.create(date=date, cargo_type=rate["cargo_type"], rate=rate["rate"])

                total += 1

        return {"all": total, "changed": changed}
    
    @classmethod
    async def calculate_insurance(cls, date: datetime.date, cargo_type: str):
        rate = await Rates.filter(date=date, cargo_type=cargo_type).first().values('rate')
        return rate
    
    @classmethod
    async def delete_rates(cls, date: datetime.date = None, rate_id: int = None) -> int or None:
        if rate_id:
            rate_obj = await Rates.filter(id=rate_id).first()

            if rate_obj:
                await rate_obj.delete()
                return 1

        elif date:

            rate_objs = await Rates.filter(date=date).all()

            if rate_objs:
                for rate in rate_objs:
                    await rate.delete()
                return 1

        return 0
    
    @classmethod
    async def update_rates(cls, date: datetime.date, cargo_type: str, rate: float):
        rate_obj = await Rates.filter(date=date, cargo_type=cargo_type).first()

        if rate_obj:
            rate_obj.rate = rate
            await rate_obj.save()
            return rate_obj
        
    @classmethod
    async def get_rates(cls, date: datetime.date = None):
        rates = await Rates.filter(date=date).all() if date else await Rates.all()

        rates_dict = {}
        for rate in rates:
            rates_dict.setdefault(rate.date, []).append({"cargo_type": rate.cargo_type, "rate": str(rate.rate)})

        return rates_dict