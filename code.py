import json
import requests
import unicodedata
import itertools

email = "leoperr@gmail.com"
password = "leo64839"

class WWENetwork():
    stream_url = "https://dce-frontoffice.imggaming.com/api/v2/stream/{id}"
    live_url = "https://dce-frontoffice.imggaming.com/api/v2/event/live"
    login_url = "https://dce-frontoffice.imggaming.com/api/v2/login"
    API_KEY = "cca51ea0-7837-40df-a055-75eb6347b2e7"

    def request(self, method, url, **kwargs):
        headers = kwargs.pop("headers", {})
        headers.update({"x-api-key": self.API_KEY,
                        "Origin": "https://watch.wwe.com",
                        "Referer": "https://watch.wwe.com/signin",
                        "Accept": "application/json",
                        "Realm": "dce.wwe"})
        if self.auth_token:
            headers["Authorization"] = "Bearer {0}".format(self.auth_token)

        if method == 'POST' or method == 'post':
            res = requests.post(url, headers=headers, **kwargs)
        else:
            res = requests.get(url, headers=headers, **kwargs)
        data = res.json()

        if "status" in data and data["status"] != 200:
            log.debug("API request failed: {0}:{1} ({2})".format(data["status"], data.get("code"), "; ".join(data.get("messages", []))))
        return data

    def login(self, email, password):
        data = self.request('POST', self.login_url,
                            data=json.dumps({"id": email, "secret": password}),
                            headers={"Content-Type": "application/json"})
        if "authorisationToken" in data:
            self.auth_token = data["authorisationToken"]

        return self.auth_token

    def __init__(self):
        self.auth_token = None

    def get_live_id(self):
        res = self.request('GET', self.live_url)
        for event in res.get('events', []):
            return "event/{sportId}/{propertyId}/{tournamentId}/{id}".format(**event)

obj = WWENetwork()
obj.login(email, password)
date = obj.get_live_id()
newUrl = obj.stream_url.format(**{"id":date})
getData = obj.request("GET", newUrl)
videoURL = getData['playerUrlCallback']
dataToM3U8 = obj.request("GET", videoURL)
manifestURL = dataToM3U8['hlsUrl']
print(manifestURL)
