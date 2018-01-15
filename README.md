# Mycroft Backend

Personal mycroft backend alternative to mycroft.home, written in flask

# UNDER CONSTRUCTION

# Status

you can run it, but why would you before it's finished?

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


start your backend by running python main.py


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


    from src.api import BackendMycroftAPI

    ap = BackendMycroftAPI("admin_key")

    print ap.pair("KHSCLA", "489e9dcb-d657-49c0-99c2-1e0f7a8f602e")


# TODOS

- skill settings

- wolfram alpha api

- weather api

- web ui

- everything else
