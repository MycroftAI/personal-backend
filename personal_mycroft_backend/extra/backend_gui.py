# Copyright 2019 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
try:
    import webview
except ImportError:
    print("ERROR: run pip install pywebview")
    try:
        import gi
    except ImportError:
        print("ERROR: run pip install pygobject")
        print("WARNING - needed system packages: sudo apt install "
              "python3-pyqt5 python3-pyqt5.qtwebkit libqt5webkit5-dev "
              "libgirepository1.0-dev")
    raise

from personal_mycroft_backend.settings import SSL, WEBSITE_PORT
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
