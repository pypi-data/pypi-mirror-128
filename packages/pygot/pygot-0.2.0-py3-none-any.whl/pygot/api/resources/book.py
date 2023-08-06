from simple_rest_client.resource import Resource


class Book(Resource):
    actions = {
        "list": {"method": "GET", "url": "books"},
        "show": {"method": "GET", "url": "books/{}"},
    }
