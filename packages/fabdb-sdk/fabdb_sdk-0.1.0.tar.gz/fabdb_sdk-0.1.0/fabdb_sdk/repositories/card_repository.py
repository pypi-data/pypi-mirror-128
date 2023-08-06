from collections import namedtuple

from fabdb_sdk.helpers.api_client import ApiClient


class CardRepository:
    def get_all(self):
        response = ApiClient().request("/cards")
        return response["data"]

    def get_card(self, cardname):
        response = ApiClient().request("/cards/" + cardname)
        return self.__convert_to_object("Card", response)

    def __convert_to_object(self, object_name, dictionary):
        return namedtuple(object_name, dictionary.keys())(*dictionary.values())
