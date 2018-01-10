# Mycroft Backend

Personal mycroft backend alternative to mycroft.home, written in flask

# UNDER CONSTRUCTION

# usage


wait until it is finished


change url in "server" section in your default mycroft config

     // Address of the REMOTE server
      // Override: none
      "server": {
        "url": "https://127.0.0.1:6712",
        "version": "v0.1",
        "update": true,
        "metrics": true
      },


start your backend by running

    python main.py


# Features


- get location

- geoip location

- get settings

- whole pairing process



# remote admin api


quickly pair a device by


    from src.api import BackendMycroftAPI

    ap = BackendMycroftAPI("admin_key")

    print ap.pair("BBDYIZU9", "090422ad-ba2a-49ea-98ba-e39b41471368")


# TODOS


- set up a database

- everything else
