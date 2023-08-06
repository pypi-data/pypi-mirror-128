from geld.common.validators import (
    amount_validator,
    currency_code_validator,
    date_validator,
)


def validate_currency_conversion_data(func):
    def _validate_entry_values(
        self, from_currency, to_currency, amount=1, date="latest"
    ):
        from_currency = currency_code_validator(from_currency)
        to_currency = currency_code_validator(to_currency)
        amount = amount_validator(amount)
        date = date_validator(date)
        return func(self, from_currency, to_currency, amount, date)

    return _validate_entry_values
