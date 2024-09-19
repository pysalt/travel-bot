from logging import getLogger

import httpx
from httpx import HTTPStatusError, RequestError

logger = getLogger('http_client')


class BaseClientError(BaseException):
    pass


class APIRequestError(BaseClientError):
    pass


class APIUnavailableError(BaseClientError):
    pass


class BaseClient:
    def __init__(self, base_url: str | None = None, timeout: float = 10.0):
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def get(self, path, params: dict | None = None) -> list | dict:
        try:
            response = await self._client.get(path, params=params)
            response.raise_for_status()
        except HTTPStatusError:
            logger.exception('Error response from API: %s', path)
            raise APIRequestError()
        except RequestError:
            logger.exception('API is unavailable: %s', path)
            raise APIUnavailableError()

        return response.json()

    async def close(self):
        await self._client.aclose()
