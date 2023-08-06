import httpx

from .book import Book
from .character import Character
from .house import House


def fetch_resources(api, endpoint, schema):
    endpoint = getattr(api, endpoint)
    method = getattr(endpoint, "list")

    resources = method()
    yield from schema.load(resources.body)

    next_link = resources.client_response.links["next"]

    next = True
    while next:
        response = httpx.get(next_link["url"])
        next_link = response.links.get("next", None)
        if next_link:
            next = True
            yield from response.json()
        else:
            next = False


def init_api(api):
    api.add_resource(resource_name="books", resource_class=Book)
    api.add_resource(resource_name="characters", resource_class=Character)
    api.add_resource(resource_name="houses", resource_class=House)
