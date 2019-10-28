# Personal Mycroft Backend


Personal mycroft backend alternative to mycroft.home, written in flask

Official mycroft backend has been open sourced, read the [blog post](https://mycroft.ai/blog/open-sourcing-the-mycroft-backend/)

This repo is an alternative to the backend meant for personal usage, eventually this will become an out of the box solution to run completely offline

If you need to manage multiple user accounts this project is not for you!

# UNDER CONSTRUCTION

Mycroft Backend API docs can be found [here](https://mycroftai.github.io/mycroft-api-docs-renderer/)

NOTE: this is the backend only, the plan is to make it compatible with the official [selene ui](https://github.com/MycroftAI/selene-ui)

## Install

from source

    git clone https://github.com/MycroftAI/personal-backend
    cd personal-backend
    pip install .

from pip

    pip install git+https://github.com/MycroftAI/personal-backend.git
    
configure backend by editing/creating ~/.mycroft/personal_backend/personal_backend.conf

    {
    "backend_port": 6712,
    "ssl": true,
    "ssl_key": "/home/user/.mycroft/personal_backend/certs/MycroftPersonalServer.key",
    "ssl_cert": "/home/user/.mycroft/personal_backend/certs/MycroftPersonalServer.crt",
    "mail_port": 465,
    "mail_server": "smtp.googlemail.com",
    "mail_user": "xxx@gmail.com",
    "mail_password": "xxx"
    }

change url in "server" section in your default mycroft config

     // Address of the REMOTE server
      // Override: none
      "server": {
        "url": "http://0.0.0.0:6712",
        "version": "v1",
        "update": true,
        "metrics": true
      },

if you want to perform TTS in the backend side change the mimic2 url

    "tts": {
        "module": "mimic2",
        "mimic2": {
          "lang": "en-us",
          // this will allow you to use any number of tts on personal backend
          // currently supported: google, mimic2
          // "url": "http://0.0.0.0:6712/synthesize/google/female/en-us?text=",
          "url": "http://0.0.0.0:6712/synthesize/mimic2/kusal/en-us?text=",
          "preloaded_cache": "/opt/mycroft/preloaded_cache/google"
        },

## usage

start backend 

    from personal_mycroft_backend.backend import start_backend
    
    start_backend()

more examples [here](examples)

## Features / Routes


- get location

- geoip location default

- get config

- get device settings

- patch device settings

- pairing process

- send mail

- multiple STT engines supported (google, wit, ibm, kaldi, bing, houndify, govivace, deepspeech)

- sql database

- remote TTS, mocking mimic2 api:
    - google TTS
    - Mimic2 Proxy

# Credits

Thanks goes out to JarbasAI for creating this initial implementation. You can find the archived [original repo here](https://github.com/JarbasAl/ZZZ_personal-mycroft-backend).

