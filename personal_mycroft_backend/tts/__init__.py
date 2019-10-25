import os
import re
import hashlib
import os.path
from abc import ABCMeta

from personal_mycroft_backend.utils.cache import (
    get_cache_directory, curate_cache
)


class TTS(metaclass=ABCMeta):
    """
    TTS abstract class to be implemented by all TTS engines.

    It aggregates the minimum required parameters and exposes
    ``execute(sentence)`` and ``validate_ssml(sentence)`` functions.

    Args:
        lang (str):
        config (dict): Configuration for this specific tts engine
        validator (TTSValidator): Used to verify proper installation
        phonetic_spelling (bool): Whether to spell certain words phonetically
        ssml_tags (list): Supported ssml properties. Ex. ['speak', 'prosody']
    """
    works_offline = True
    voices = []
    audio_ext = "mp3"

    def __init__(self, lang="en-us", config=None, validator=None, audio_ext='wav',
                 phonetic_spelling=True, ssml_tags=None):
        config = config or {}
        super(TTS, self).__init__()
        self.bus = None  # initalized in "init" step
        self.lang = lang or 'en-us'
        self.config = config
        self.validator = validator
        self.phonetic_spelling = phonetic_spelling
        self.audio_ext = audio_ext
        self.ssml_tags = ssml_tags or []
        self.voice = "defaultVoice"
        self.filename = '/tmp/tts.mp3'
        self.clear_cache()
        self.tts_name = type(self).__name__

    def get_tts(self, sentence, mp3_file):
        """
            Abstract method that a tts implementation needs to implement.
            Should get data from tts.

            Args:
                sentence(str): Sentence to synthesize
                mp3_file(str): output file

            Returns:
                tuple: (wav_file, phoneme)
        """
        pass

    def execute(self, sentence, voice=None, lang=None):
        self.lang = lang or self.lang
        key = str(hashlib.md5(sentence.encode('utf-8', 'ignore')).hexdigest())
        voice = voice or self.voice
        wav_file = os.path.join(get_cache_directory("tts"),
                                "{tts}_{voice}_{lang}_".format(voice=voice,
                                                               lang=self.lang,
                                                               tts=self.__class__.__name__) + key + '.' + self.audio_ext)
        if not os.path.exists(wav_file):
            wav_file, phonemes = self.get_tts(sentence, wav_file)
        return wav_file

    def modify_tag(self, tag):
        """Override to modify each supported ssml tag"""
        return tag

    @staticmethod
    def remove_ssml(text):
        return re.sub('<[^>]*>', '', text).replace('  ', ' ')

    def validate_ssml(self, utterance):
        """
            Check if engine supports ssml, if not remove all tags
            Remove unsupported / invalid tags

            Args:
                utterance(str): Sentence to validate

            Returns: validated_sentence (str)
        """
        # if ssml is not supported by TTS engine remove all tags
        if not self.ssml_tags:
            return self.remove_ssml(utterance)

        # find ssml tags in string
        tags = re.findall('<[^>]*>', utterance)

        for tag in tags:
            if any(supported in tag for supported in self.ssml_tags):
                utterance = utterance.replace(tag, self.modify_tag(tag))
            else:
                # remove unsupported tag
                utterance = utterance.replace(tag, "")

        # return text with supported ssml tags only
        return utterance.replace("  ", " ")

    def clear_cache(self):
        """ Remove all cached files. """
        if not os.path.exists(get_cache_directory('tts')):
            return
        for d in os.listdir(get_cache_directory("tts")):
            dir_path = os.path.join(get_cache_directory("tts"), d)
            if os.path.isdir(dir_path):
                for f in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, f)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
            # If no sub-folders are present, check if it is a file & clear it
            elif os.path.isfile(dir_path):
                os.unlink(dir_path)


class TTSFactory:
    from personal_mycroft_backend.tts.google_tts import GoogleTTS

    CLASSES = {
        "google": GoogleTTS
    }

    @staticmethod
    def create(tts="google"):
        clazz = TTSFactory.CLASSES.get(tts)
        return clazz()


if __name__ == "__main__":
    tts = TTSFactory.create("google")
    from os.path import basename

    print(basename(tts.execute("hello world")))
