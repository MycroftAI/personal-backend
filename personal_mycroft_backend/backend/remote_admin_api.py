import requests
from requests.exceptions import ConnectionError

from personal_mycroft_backend.settings import DEBUG, SSL


class BackendMycroftAPI(object):
    def __init__(self, api, lang="en-us", url="https://0.0.0.0:6712/v0.1/",
                 debug=DEBUG, ssl=SSL):
        if not ssl:
            url = url.replace("https", "http")
        if debug:
            # filter warnings, TODO this should be removed once we stop using self signed certs
            from requests.packages.urllib3.exceptions import \
                InsecureRequestWarning

            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self.api = api
        self.headers = {"Authorization": self.api.encode("utf-8")}
        self.lang = lang
        self.url = url
        self.timeout = 10
        self.wait_time = 0.5

    def pair(self, code, uuid, mail, name="jarbas"):
        ''' add a new user, requires admin api '''
        try:
            response = requests.put(
                self.url+"pair/"+code+"/"+uuid+"/"+name+"/"+mail,
                headers=self.headers, verify=not DEBUG
            )
            try:
                return response.json()
            except:
                print(response.text)
                raise ValueError("Invalid admin api key")
        except ConnectionError as e:
            raise ConnectionError("Could not connect: " + str(e))


if __name__ == "__main__":
    ap = BackendMycroftAPI("admin_key")
    username = "jarbasX"
    code = "XQFTNM"
    uuid = "cc3524c7-ff52-42b3-af8f-de89249b19c8"
    mail = "fakemail2@not_real.com"
    print(ap.pair(code, uuid, mail, username))


