# Mycroft Backend


Personal mycroft backend alternative to mycroft.home, written in flask

# UNDER CONSTRUCTION

![](media/personalbackend.jpg)

you can run it, but why would you before it's finished?

# usage


wait until it is finished


configure backend by editing settings.py

    SECRET_KEY = 'MY_PRECIOUS_SECRET_KEY'
    SECURITY_PASSWORD_SALT = 'MY_TABLE_SALT'
    API_VERSION = "v0.1"
    SQL_ADMINS_URI = "sqlite:///database/admins.db"
    SQL_DEVICES_URI = "sqlite:///database/devices.db"
    DEBUG = True
    SSL = False
    SSL_CERT = ""
    SSL_KEY = ""
    BACKEND_PORT = 6712
    WEBSITE_PORT = 5000
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "will.send.from.here@gmail.com"
    MAIL_PASSWORD = "not a passwd"
    MAIL_DEFAULT_SENDER = "will.send.from.here@gmail.com"

change url in "server" section in your default mycroft config

     // Address of the REMOTE server
      // Override: none
      "server": {
        "url": "https://127.0.0.1:6712",
        "version": "v0.1",
        "update": true,
        "metrics": true
      },


start your backend by running start_backend.py, start website by running start_frontend.py


# Features


- get location

- geoip location default

- get config

- get device settings

- patch device settings

- pairing process

- store metrics (integrating into frontend, sql db and api endpoints functional)

- send mail

- STT using deepspeech or google (testing )

- sql database

- user email confirmation

- website (status: WIP)

- local browserless GUI if running on same machine (testing)



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

- STT json settings in db (for google cloud stt engine)

- skill settings

- wakeword upload

- wolfram alpha api

- weather api

- everything else i forgot

- new functionality
    - user voice print from uploaded utterances / wakewords
    - train snowboy models