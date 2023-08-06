from geld.common.base_client import BaseClient
from datetime import date
from decimal import Decimal

class SyncClientBase(BaseClient):   
    def convert_currency(from_currency: str, to_currency: str, amount: Decimal, date: date = None):
        raise NotImplemented
