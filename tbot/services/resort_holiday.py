from urllib.parse import urljoin

from tbot.settings import settings


class ResortHolidayClient:
    async def get_current_currency(self):
        path = 'currency/current/'
        url = urljoin(settings.resort_holiday.url, path)
        return url
