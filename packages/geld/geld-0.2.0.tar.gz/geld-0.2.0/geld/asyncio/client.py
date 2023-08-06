from geld.common.decorators import validate_currency_conversion_data
from geld.common.exceptions import APICallError
from geld.asyncio.base import AsyncClientBase

from decimal import Decimal

import aiohttp


class AsyncClient(AsyncClientBase):
    @validate_currency_conversion_data
    async def convert_currency(
        self,
        from_currency: str,
        to_currency: str,
        amount: Decimal = 1,
        date: str = "latest",
    ):
        url = self.helper.get_url(self.base_url, date)
        params = self.helper.get_params(from_currency, to_currency)
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, params=params)
            if not response.status == 200:
                raise APICallError
        rate = await self.helper.get_rate_from_response(response, to_currency)
        converted_amount = amount * rate
        return converted_amount
