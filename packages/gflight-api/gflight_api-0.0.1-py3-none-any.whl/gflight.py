import requests
import json


class API:
    URL = "https://fly-sujal.herokuapp.com/"
    QUERY_URL = URL + "?oci={}&oco={}&dci={}&dco={}&dd={}"

    def __init__(self):
        self.session = requests.Session()

    @staticmethod
    def validate_query_params(params):
        assert len(params) == 5

    def fetch(self, query_params):
        self.validate_query_params(query_params)
        data = self.session.get(self.QUERY_URL.format(*query_params))

        return json.loads(data.content.decode())
