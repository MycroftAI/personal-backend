from src.base import *
from flask import redirect, url_for, request, Response

from speech_recognition import Recognizer

recognizer = Recognizer()


@app.route("/"+API_VERSION+"/stt", methods=['POST'])
@noindex
@donation
@requires_auth
def stt(uuid):
    audio = request.data
    lang = request.query.get("lang", "en-US")
    limit = request.query.get("limit", 1)
    utterance = recognizer.recognize_google(audio, language=lang)
    return utterance


if __name__ == "__main__":
    global app
    port = 6712
    start(app, port)
