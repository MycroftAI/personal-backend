from backend import app, API_VERSION, USE_DEEPSPEECH
from backend.decorators import noindex, donation, requires_auth
from flask import request
from tempfile import TemporaryFile

if USE_DEEPSPEECH:
    from extra.deepspeech_stt import DeepSpeechSTT
    stt = DeepSpeechSTT()
    recognize = stt.recognize
else:
    from speech_recognition import Recognizer, AudioFile
    recognizer = Recognizer()
    recognize = recognizer.recognize_google


@app.route("/"+API_VERSION+"/stt", methods=['POST'])
@noindex
@donation
@requires_auth
def stt():
    flac_audio = request.data
    lang = request.args["lang"] or "en-us"

    with TemporaryFile() as fp:
        fp.write(flac_audio)
        with AudioFile(fp) as source:
            audio = recognizer.record(source)  # read the entire audio file

        utterance = recognize(audio, language=lang)
    return utterance
