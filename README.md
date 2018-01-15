# Mycroft Backend

Personal mycroft backend alternative to mycroft.home, written in flask

# UNDER CONSTRUCTION

![](media/personalbackend.jpg)

you can run it, but why would you before it's finished?

# usage


wait until it is finished


configure backend by editing settings.py

    API_VERSION = "v0.1"
    MAIL = "mail to be used by your devices"
    PASSWORD = "mail password"
    SQL_ADMINS_URI = "sqlite:///database/admins.db"
    SQL_DEVICES_URI = "sqlite:///database/devices.db"
    DEBUG = True
    SSL = False
    SSL_CERT = "path/to.crt"
    SSL_KEY = "path/to.key"
    BACKEND_PORT = 6712
    WEBSITE_PORT = 5000

change url in "server" section in your default mycroft config

     // Address of the REMOTE server
      // Override: none
      "server": {
        "url": "https://127.0.0.1:6712",
        "version": "v0.1",
        "update": true,
        "metrics": true
      },


start your backend by running main.py, start website by running website.py


# Features


- get location

- geoip location default

- get config

- get device settings

- patch device settings

- pairing process

- store metrics

- send mail

- STT using google default key

- sql database


# remote admin api


quickly pair a device by


    from api import BackendMycroftAPI

    ap = BackendMycroftAPI("admin_key")
    username = "jarbasX"
    code = "XQFTNM"
    uuid = "cc3524c7-ff52-42b3-af8f-de89249b19c8"
    mail = "fakemail2@not_real.com"
    print ap.pair(code, uuid, mail, username)

# TODOS

- skill settings

- wolfram alpha api

- weather api

- web ui

- everything else
