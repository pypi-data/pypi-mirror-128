from geld.common import BASE_URL
from geld.common.exceptions import BaseUrlNotDefined
from geld.common.helpers import ClientHelper
from geld.common.singleton import SingletonMeta


class BaseClient(metaclass=SingletonMeta):
    base_url = BASE_URL
    helper = ClientHelper

    def __init__(self):
        if not self.base_url:
            raise BaseUrlNotDefined
