import json

from tortoise import Tortoise

from app.models.models import Rates
from app.services.insurance import InsuranceService


class DatabaseService:

    def __init__(self, debug: bool = True,
                 postgre_con: str = "postgres://postgres:pass@db.host:5432/somedb") -> None:
        
        self.db_url = "sqlite://db.sqlite3" if debug else postgre_con

    async def init_db(self) -> None:
        await Tortoise.init(
            db_url=self.db_url,
            modules={"models": ["app.models.models"]},
        )
        await Tortoise.generate_schemas()

        contains_data: bool = await Rates.all().exists()
        if not contains_data:
            with open('app/config/test_rates.json', encoding="utf-8") as file:
                start_rates = json.load(file)
            await InsuranceService.populate_db(start_rates)

    @classmethod
    async def close_db(cls) -> None:
        await Tortoise.close_connections()
