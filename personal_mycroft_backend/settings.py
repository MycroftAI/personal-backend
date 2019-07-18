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
from os.path import exists, expanduser, join
from os import makedirs
from personal_mycroft_backend.utils.self_signed import create_self_signed_cert
from personal_mycroft_backend.utils.json_helper import load_commented_json, \
    merge_dict
import json

DATA_PATH = join(expanduser("~"), ".mycroft", "personal_backend")
if not exists(DATA_PATH):
    makedirs(DATA_PATH)

CONF_FILE = join(DATA_PATH, "personal_backend.conf")
if exists(CONF_FILE):
    conf = load_commented_json(CONF_FILE)
else:
    conf = {}

DEBUG = conf.get("debug", False)
USE_DEEPSPEECH = conf.get("deepspeech", False)

# SQL
SQL_ADMINS_URI = conf.get("admins_db",
                          'sqlite:///' + join(DATA_PATH, 'admins.db'))
SQL_DEVICES_URI = conf.get("devices_db",
                           'sqlite:///' + join(DATA_PATH, 'devices.db'))

# SSL
SSL = conf.get("ssl", False)
SSL_CERT = conf.get("ssl_cert")
SSL_KEY = conf.get("ssl_key")
if not exists(SSL_CERT) or not exists(SSL_KEY):
    SSL_CERT, SSL_KEY = create_self_signed_cert(join(DATA_PATH, "certs"),
                                                "MycroftPersonalServer")

# PERSONAL SERVER
API_VERSION = conf.get("api_version", "v0.1")
BACKEND_PORT = conf.get("backend_port", 6712)
WEBSITE_PORT = conf.get("website_port", 5000)
SECRET_KEY = conf.get("secret_key", 'MY_PRECIOUS_SECRET_KEY')
SECURITY_PASSWORD_SALT = conf.get("salt", 'MY_TABLE_SALT')

# EMAIL
MAIL_SERVER = conf.get("mail_server", 'smtp.googlemail.com')
MAIL_PORT = conf.get("mail_port", 465)
MAIL_USE_TLS = conf.get("mail_tls", False)
MAIL_USE_SSL = conf.get("mail_ssl", True)
MAIL_USERNAME = conf.get("mail_user", "xxx@gmail.com")
MAIL_PASSWORD = conf.get("mail_password", "xxx")
MAIL_DEFAULT_SENDER = conf.get("mail_sender", MAIL_USERNAME)

STT_CONFIG = conf.get("stt") or {"module": "google", "google": {}}

LANG = conf.get("lang", "en-us")

def create_conf_file():
    default_conf = {
        "lang": LANG,
        "stt": STT_CONFIG,
        "backend_port": BACKEND_PORT,
        "website_port": WEBSITE_PORT,
        "secret_key": SECRET_KEY,
        "salt": SECURITY_PASSWORD_SALT,
        "ssl": SSL,
        "ssl_cert": SSL_CERT,
        "ssl_key": SSL_KEY,
        "mail_user": MAIL_USERNAME,
        "mail_password": MAIL_PASSWORD,
        "mail_server": MAIL_SERVER,
        "mail_port": MAIL_PORT
    }
    if exists(CONF_FILE):
        merge_dict(default_conf, load_commented_json(CONF_FILE))
    with open(CONF_FILE, "w") as f:
        f.write(json.dumps(default_conf, indent=4))


if not exists(CONF_FILE):
    create_conf_file()
