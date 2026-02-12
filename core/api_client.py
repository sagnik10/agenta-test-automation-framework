import requests

class APIClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.session = requests.Session()
        if token:
            self.session.headers.update({'Authorization': f'Bearer {token}'})

    def post(self, endpoint, payload, **kwargs):
        return self.session.post(self.base_url + endpoint, json=payload, **kwargs)

    def get(self, endpoint, **kwargs):
        return self.session.get(self.base_url + endpoint, **kwargs)
