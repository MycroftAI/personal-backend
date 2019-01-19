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
from timeit import default_timer as timer
from os.path import exists, join, dirname
from os import makedirs
from time import sleep
from personal_mycroft_backend.settings import DATA_PATH, STT_CONFIG
from personal_mycroft_backend.utils.download import download, untar

try:
    from deepspeech.model import Model
except ImportError:
    print("could not import deep speech, \n run pip install "
          "deepspeech")
    raise


class DeepSpeechV01STT(object):
    config = STT_CONFIG.get("deepspeech", {})

    # Model paths
    DEEPSPEECH_DATADIR = join(DATA_PATH, "deepspeech", "v01")
    if not exists(DEEPSPEECH_DATADIR):
        makedirs(DEEPSPEECH_DATADIR)
    MODEL_DOWNLOAD_URL = "https://github.com/mozilla/DeepSpeech/releases/download/v0.1.0/deepspeech-0.1.0-models.tar.gz"

    MODEL_PATH = config.get("model", join(DEEPSPEECH_DATADIR,
                                          "output_graph.pb"))
    LM_PATH = config.get("lm", join(DEEPSPEECH_DATADIR, "lm.binary"))
    TRIE_PATH = config.get("trie", join(DEEPSPEECH_DATADIR, "trie"))
    ALPHABET_PATH = config.get("alphabet", join(DEEPSPEECH_DATADIR,
                                                "alphabet.txt"))

    # These constants control the beam search decoder

    # Beam width used in the CTC decoder when building candidate transcriptions
    BEAM_WIDTH = config.get("beam_width", 500)

    # The alpha hyperparameter of the CTC decoder. Language Model weight
    LM_WEIGHT = config.get("lm_weight", 1.75)

    # The beta hyperparameter of the CTC decoder. Word insertion weight (penalty)
    WORD_COUNT_WEIGHT = config.get("word_count_weight", 1.00)

    # Valid word insertion weight. This is used to lessen the word insertion penalty
    # when the inserted word is part of the vocabulary
    VALID_WORD_COUNT_WEIGHT = config.get("valid_word_count_weight", 1.00)

    # These constants are tied to the shape of the graph used (changing them changes
    # the geometry of the first layer), so make sure you use the same constants that
    # were used during training

    # Number of MFCC features to use
    N_FEATURES = config.get("n_features", 26)

    # Size of the context window used for producing timesteps in the input vector
    N_CONTEXT = config.get("n_context", 9)

    def __init__(self):
        self.downloaded = False
        self.dl = None
        if self.is_ready(False):
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
        print('Loading model from file %s' % (self.MODEL_PATH))
        model_load_start = timer()
        self.ds = Model(self.MODEL_PATH, self.N_FEATURES, self.N_CONTEXT,
                        self.ALPHABET_PATH, self.BEAM_WIDTH)

        model_load_end = timer() - model_load_start
        print('Loaded model in %0.3fs.' % (model_load_end))

        print('Loading language model from files %s %s' % (
            self.LM_PATH, self.TRIE_PATH))
        lm_load_start = timer()
        self.ds.enableDecoderWithLM(self.ALPHABET_PATH, self.LM_PATH,
                                    self.TRIE_PATH,
                                    self.LM_WEIGHT,
                                    self.WORD_COUNT_WEIGHT,
                                    self.VALID_WORD_COUNT_WEIGHT)
        lm_load_end = timer() - lm_load_start
        print('Loaded language model in %0.3fs.' % (lm_load_end))

    def is_ready(self, is_critical=False):
        try:
            if not exists(self.MODEL_PATH):
                raise AssertionError(
                    self.MODEL_PATH + " does not exist, download a "
                                      "pre-trained model with \n wget -O -" +
                    self.MODEL_DOWNLOAD_URL + "| tar xvfz -")
            if not exists(self.LM_PATH):
                raise AssertionError("language model does not exist")

            if not exists(self.ALPHABET_PATH):
                raise AssertionError(
                    "alphabet configuration file does not exist")

            if not exists(self.TRIE_PATH):
                raise AssertionError("language model trie does not exist")
        except:
            if is_critical:
                raise
            return False
        return True

    def download(self):
        print("starting model download")
        target_folder = self.DEEPSPEECH_DATADIR
        self.dl = download(self.MODEL_DOWNLOAD_URL, target_folder,
                           self._extract)

    def _extract(self, target_folder=None):
        target_folder = target_folder or self.DEEPSPEECH_DATADIR
        print("model downloaded, extracting files")
        untar(join(target_folder, self.MODEL_DOWNLOAD_URL.split("/")[-1]),
              target_folder, True)
        print("model ready")
        self.downloaded = True

    def recognize(self, audio, language="en-us"):
        if not language.startswith("en"):
            raise NotImplementedError("the only supported language is "
                                      "english")
        return self.ds.stt(audio.get_wav_data(), 16000)


class DeepSpeechV02STT(DeepSpeechV01STT):
    DEEPSPEECH_DATADIR = join(DATA_PATH, "deepspeech", "v02")
    if not exists(DEEPSPEECH_DATADIR):
        makedirs(DEEPSPEECH_DATADIR)
    MODEL_DOWNLOAD_URL = "https://github.com/mozilla/DeepSpeech/releases/download/v0.2.0/deepspeech-0.2.0-models.tar.gz"


class DeepSpeechV03STT(DeepSpeechV01STT):
    DEEPSPEECH_DATADIR = join(DATA_PATH, "deepspeech", "v03")
    if not exists(DEEPSPEECH_DATADIR):
        makedirs(DEEPSPEECH_DATADIR)
    MODEL_DOWNLOAD_URL = "https://github.com/mozilla/DeepSpeech/releases/download/v0.3.0/deepspeech-0.3.0-models.tar.gz"
