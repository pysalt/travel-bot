from pydantic import BaseModel, TypeAdapter

from tbot.services.base_http import BaseClient


class Currency(BaseModel):
    currencyISO: str
    rate: str

currency_parser = TypeAdapter(list[Currency])


class ResortHolidayClient(BaseClient):
    async def get_current_currency(self) -> list[Currency]:
        path = '/currency/current/'
        response = await self.get(path)
        return currency_parser.validate_python(response)
