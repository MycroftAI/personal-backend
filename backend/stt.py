from backend import app, API_VERSION
from backend.decorators import noindex, donation, requires_auth
from flask import redirect, url_for, request, Response

from speech_recognition import Recognizer, AudioFile

recognizer = Recognizer()


@app.route("/"+API_VERSION+"/stt", methods=['POST'])
@noindex
@donation
@requires_auth
def stt():
    flac_audio = request.data
    lang = request.args["lang"]

    with open("stt.flac", "r+b") as f:
        f.write(flac_audio)
    with AudioFile("stt.flac") as source:
        audio = recognizer.record(source)  # read the entire audio file

    utterance = recognizer.recognize_google(audio, language=lang)
    return utterance
