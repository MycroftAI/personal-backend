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
from pydub import AudioSegment
import base64
from personal_mycroft_backend.backend.decorators import noindex, requires_auth
from personal_mycroft_backend.tts import TTSFactory
from personal_mycroft_backend.utils import nice_json

from flask import send_file, request

tts = TTSFactory.create()


def convert(mp3):
    sound = AudioSegment.from_mp3(mp3)
    sound.export(mp3.replace(".mp3", ".wav"), format="wav")
    return mp3.replace(".mp3", ".wav")


def build_response(audio_file, visimes=None):
    if visimes is not None:
        with open(audio_file, "rb") as f:
            audio_data = f.read()
        encoded_audio = base64.b64encode(audio_data)
        res = {
            "audio_base64": encoded_audio.decode("utf-8"),
            "visimes": visimes
        }
        return nice_json(res)
    else:
        return send_file(
            audio_file,
            mimetype="audio/wav")


def get_tts_routes(app):
    @app.route("/synthesize/google/<voice>/<lang>", methods=['GET'])
    @noindex
    # @requires_auth
    def google(voice, lang):
        text = request.args.get('text')
        return_visimes = request.args.get('visimes')
        path_to_file = tts.execute(text, voice=voice, lang=lang)
        if tts.audio_ext != "wav":
            # since we are mocking mimic2 we must return as wav format
            path_to_file = convert(path_to_file)
        visimes = []  # TODO visime support?
        return build_response(path_to_file, visimes if return_visimes else None)

    return app
