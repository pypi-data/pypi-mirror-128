import json
from decimal import Decimal


class ClientHelper:
    @staticmethod
    def get_url(base_url, date: str):
        return f"{base_url}/{date}/"

    @staticmethod
    def get_params(from_currency: str, to_currency: str):
        return {
            "base": from_currency,
            "symbols": to_currency,
        }

    @staticmethod
    def get_rate_from_response(response: dict, to_currency: str):
        data = json.loads(response.text)
        rate = Decimal(data["rates"][to_currency])
        return rate


class AsynClientHelper(ClientHelper):
    @staticmethod
    async def get_rate_from_response(response: dict, to_currency: str):
        text = await response.text()
        data = json.loads(text)
        rate = Decimal(data["rates"][to_currency])
        return rate
