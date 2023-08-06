# -*- coding: utf-8 -*-

import functools
import requests

from fabdb_sdk.config import __baseurl__
from fabdb_sdk.exceptions.not_found_exception import NotFoundException


class ApiClient:
    def __init__(self):
        self.__base_url = __baseurl__
        self.__client = requests.Session()
        self.__client.request = functools.partial(
            self.__client.request,
            timeout=3
        )

    def request(self, endpoint):
        try:
            response = self.__client.get(
                self.__prepare_url(endpoint),
                headers={"Accept": "application/json"}
            )
            if response.status_code == 404:
                raise NotFoundException("not found")

            return response.json()
        except Exception as e:
            raise e

    def __prepare_url(self, endpoint):
        return self.__base_url + endpoint
