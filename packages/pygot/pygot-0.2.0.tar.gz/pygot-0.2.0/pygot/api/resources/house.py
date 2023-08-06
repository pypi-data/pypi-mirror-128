from simple_rest_client.resource import Resource


class House(Resource):
    actions = {
        "list": {"method": "GET", "url": "houses"},
        "show": {"method": "GET", "url": "houses/{}"},
    }
