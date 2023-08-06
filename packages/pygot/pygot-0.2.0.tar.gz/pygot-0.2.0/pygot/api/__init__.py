from simple_rest_client.api import API

from pygot.api import resources, settings


def create_api() -> API:
    api = API()
    settings.init_api(api)
    resources.init_api(api)
    return api
