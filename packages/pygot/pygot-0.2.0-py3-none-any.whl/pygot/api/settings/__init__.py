def init_api(api):
    api.api_root_url = "https://www.anapioficeandfire.com/api"
    api.headers = {"Content-Type": "application/json"}
    api.json_encode_body = True
    api.timeout = None
