from src.base import *
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

    # TODO use stream directly if possible
    with open("stt_tmp.flac", "w") as f:
        f.write(flac_audio)

    with AudioFile("stt_tmp.flac") as source:
        audio = recognizer.record(source)  # read the entire audio file

    utterance = recognizer.recognize_google(audio, language=lang)
    return utterance


if __name__ == "__main__":
    global app
    port = 6712
    start(app, port)
