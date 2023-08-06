from geld.common.decorators import validate_currency_conversion_data
from geld.common.exceptions import APICallError
from geld.sync.base import SyncClientBase

from decimal import Decimal

import requests

class SyncClient(SyncClientBase):
    @validate_currency_conversion_data
    def convert_currency(self, from_currency: str, to_currency: str, amount: Decimal = 1, date: str = "latest"):
        url = self.helper.get_url(self.base_url, date)
        params = self.helper.get_params(from_currency, to_currency)
        response = requests.get(url, params=params)
        
        if not response.status_code == 200:
            raise APICallError

        rate = self.helper.get_rate_from_response(response, to_currency)
        converted_amount = amount * rate
        return converted_amount
