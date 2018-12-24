from __future__ import absolute_import, division

from timeit import default_timer as timer
from os.path import exists, join, dirname

from personal_mycroft_backend.extra.deepspeech_settings import *
from personal_mycroft_backend.utils.download import download, untar

try:
    from deepspeech.model import Model
except ImportError:
    print("could not import deep speech, \n run pip install "
          "deepspeech")
    raise

from time import sleep


class DeepSpeechSTT(object):
    def __init__(self):
        self.downloaded = False
        self.dl = None
        if self.is_ready():
            self.load_model()
        else:
            print("Downloading model")
            self.download()
            while not self.downloaded:
                if self.dl.done:
                    raise RuntimeError("Download failed")
                sleep(1)

            if self.is_ready(True):
                self.load_model()

    def load_model(self):
        print('Loading model from file %s' % (MODEL_PATH))
        model_load_start = timer()
        self.ds = Model(MODEL_PATH, N_FEATURES, N_CONTEXT,
                        ALPHABET_PATH, BEAM_WIDTH)

        model_load_end = timer() - model_load_start
        print('Loaded model in %0.3fs.' % (model_load_end))

        print('Loading language model from files %s %s' % (
            LM_PATH, TRIE_PATH))
        lm_load_start = timer()
        self.ds.enableDecoderWithLM(ALPHABET_PATH, LM_PATH, TRIE_PATH,
                                    LM_WEIGHT,
                                    WORD_COUNT_WEIGHT,
                                    VALID_WORD_COUNT_WEIGHT)
        lm_load_end = timer() - lm_load_start
        print('Loaded language model in %0.3fs.' % (lm_load_end))

    def is_ready(self, is_critical=False):
        try:
            if not exists(MODEL_PATH):
                raise AssertionError(MODEL_PATH + " does not exist, download a "
                                                  "pre-trained model with \n wget -O -" +
                                     MODEL_DOWNLOAD_URL + "| tar xvfz -")
            if not exists(LM_PATH):
                raise AssertionError("language model does not exist")

            if not exists(ALPHABET_PATH):
                raise AssertionError("alphabet configuration file does not exist")

            if not exists(TRIE_PATH):
                raise AssertionError("language model trie does not exist")
        except:
            if is_critical:
                raise
            return False
        return True

    def download(self):
        print("starting model download")
        target_folder = join(dirname(__file__), "deepspeech")
        self.dl = download(MODEL_DOWNLOAD_URL, target_folder, self._extract)

    def _extract(self, target_folder=join(dirname(__file__), "deepspeech")):
        print("model downloaded, extracting files")
        untar(join(target_folder, MODEL_DOWNLOAD_URL.split("/")[-1]),
              target_folder, True)
        print("model ready")
        self.downloaded = True

    def recognize(self, audio, language="en-us"):
        if not language.startswith("en"):
            raise NotImplementedError("the only supported language is "
                                      "english")
        return self.ds.stt(audio.get_wav_data(), 16000)
