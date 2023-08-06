from simple_rest_client.exceptions import NotFoundError

from pygot.api import create_api
from pygot.api.resources import fetch_resources
from pygot.models.book import BookSchema
from pygot.models.character import CharacterSchema
from pygot.models.house import HouseSchema


class Pygot:
    def __init__(self) -> None:
        self._api = create_api()

    def houses(self):
        return fetch_resources(
            api=self._api, endpoint="houses", schema=HouseSchema(many=True)
        )

    def find_house(self, params):
        return HouseSchema(many=True).load(self._api.houses.list(params=params).body)

    def house(self, id):
        try:
            return HouseSchema().load(self._api.houses.show(id).body)
        except NotFoundError:
            raise Exception("House Not Found")

    def books(self):
        return fetch_resources(
            api=self._api, endpoint="books", schema=BookSchema(many=True)
        )

    def find_book(self, params):
        return BookSchema(many=True).load(self._api.books.list(params=params).body)

    def book(self, id):
        try:
            return BookSchema().load(self._api.books.show(id).body)
        except NotFoundError:
            raise Exception("Book Not Found")

    def characters(self):
        return fetch_resources(
            api=self._api, endpoint="characters", schema=CharacterSchema(many=True)
        )

    def find_character(self, params):
        return CharacterSchema(many=True).load(
            self._api.characters.list(params=params).body
        )

    def character(self, id):
        try:
            return CharacterSchema().load(self._api.characters.show(id).body)
        except NotFoundError:
            raise Exception("Character Not Found")
