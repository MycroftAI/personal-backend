import webview
from settings import SSL, WEBSITE_PORT
from os.path import join


class BackendGUI(object):
    def __init__(self, url=None, name="Personal Mycroft Backend", ssl=SSL):
        self.url = url or "https://127.0.0.1:" + str(WEBSITE_PORT)
        self.name = name
        if not ssl:
            self.url = self.url.replace("https", "http")

    def open(self):
        webview.create_window(self.name, self.url)

    def close(self):
        webview.destroy_window()

    def goto(self, endpoint):
        webview.load_url(join(self.url, endpoint))


if __name__ == "__main__":
    browser = BackendGUI()
    browser.open()
