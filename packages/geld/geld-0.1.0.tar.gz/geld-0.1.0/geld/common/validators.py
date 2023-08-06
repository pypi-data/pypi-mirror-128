from decimal import Decimal
from geld.common.constants import CURRENCY_DATA
from geld.common.exceptions import (
    InvalidAmount,
    InvalidCurrencyCode,
    InvalidDate,
)


def currency_code_validator(currency_code):
    try:
        _ = CURRENCY_DATA[currency_code]
    except KeyError:
        raise InvalidCurrencyCode
    return currency_code


def date_validator(date):
    try:
        if not isinstance(date, str):
            date = date.isoformat()[0:10]
    except Exception:
        raise InvalidDate
    return date


def amount_validator(amount):
    try:
        if not isinstance(amount, Decimal):
            amount = Decimal(amount)
    except Exception:
        raise InvalidAmount
    return amount
