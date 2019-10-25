# Copyright 2017 Mycroft AI Inc.
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
from gtts import gTTS

from personal_mycroft_backend.tts import TTS

import logging

logging.getLogger('gtts.tts').setLevel(logging.CRITICAL)


class GoogleTTS(TTS):
    voices = ["female"]
    works_offline = False
    audio_ext = "mp3"

    def __init__(self, lang="en-us", config=None):
        super(GoogleTTS, self).__init__(lang, config, None, 'mp3')
        self.voice = "female"

    def get_tts(self, sentence, mp3_file):
        tts = gTTS(sentence, self.lang)
        tts.save(mp3_file)
        return (mp3_file, None)  # No phonemes

