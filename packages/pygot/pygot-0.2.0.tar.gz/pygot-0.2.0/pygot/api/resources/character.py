from simple_rest_client.resource import Resource


class Character(Resource):
    actions = {
        "list": {"method": "GET", "url": "characters"},
        "show": {"method": "GET", "url": "characters/{}"},
    }
