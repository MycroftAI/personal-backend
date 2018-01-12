from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship

from src.database.devices import Device, User, Skill
from src.database import Base


class Configuration(Base):
    __tablename__ = "configs"
    uuid = Column(String, ForeignKey(Device.uuid), primary_key=True)
    device = relationship(Device, back_populates="config")
    users = relationship(User, back_populates="configs")
    hotwords = relationship(Hotword, back_populates="configs")
    stt = relationship(STT, back_populates="configs")
    tts = relationship(TTS, back_populates="configs")
    sounds = relationship(Sounds, back_populates="configs")
    skills = relationship(Skill, back_populates="configs")

    lang = Column(String)
    system_unit = Column(String, default="metric")
    time_format = Column(String, default="full")
    date_format = Column(String, default="DMY")
    opt_in = Column(Boolean, default=False)
    confirm_listening = Column(Boolean, default=False)
    play_wav_cmdline = Column(String,
                              default="paplay %1 --stream-name=mycroft-voice")
    play_mp3_cmdline = Column(String, default="mpg123 %1")
    skills_dir = Column(String, default="/opt/mycroft/skills")
    skills_auto_update = Column(Boolean, default=False)
    listener_sample_rate = Column(Integer, default=16000)
    listener_channels = Column(Integer, default=1)
    record_wake_words = Column(Boolean, default=False)
    record_utterances = Column(Boolean, default=False)
    wake_word_upload = Column(Boolean, default=False)
    phoneme_duration = Column(Integer, default=120)
    listener_multiplier = Column(Float, default=1.0)
    listener_energy_ratio = Column(Float, default=1.5)
    wake_word = Column(String, default="hey mycroft")
    stand_up_word = Column(String, default="wake up")

    def __repr__(self):
        return self.uuid


class Sounds(Base):
    __tablename__ = "sounds"
    configs = relationship(Configuration, back_populates="sounds")
    path = Column(String, default="")
    name = Column(String, default="")

    def __repr__(self):
        return self.name


class Hotword(Base):
    __tablename__ = "hotwords"
    devices = relationship(Device, back_populates="hotwords")
    users = relationship(User, back_populates="hotwords")
    configs = relationship(Configuration, back_populates="hotwords")

    name = Column(String, default="wake up")
    module = Column(String, default="pocketsphinx")
    phonemes = Column(String, default="HH EY . M AY K R AO F T")
    threshold = Column(String, default="1e-90")
    hotword_lang = Column(String, default="en-us")
    active = Column(Boolean, default=False)
    listen = Column(Boolean, default=False)
    utterance = Column(String, default="")
    sound =Column(String, default="")

    def __repr__(self):
        return self.name


class STT(Base):
    __tablename__ = "stt_engines"
    configs = relationship(Configuration, back_populates="stt")
    name = Column(String, default="")
    lang = Column(String, default="en-us")
    uri = Column(String, default="")
    token = Column(String, default="")
    username = Column(String, default="")
    password = Column(String, default="")

    def __repr__(self):
        return self.name


class TTS(Base):
    __tablename__ = "tts_engines"
    configs = relationship(Configuration, back_populates="tts")
    name = Column(String, default="")
    lang = Column(String, default="en-us")
    uri = Column(String, default="")
    token = Column(String, default="")
    username = Column(String, default="")
    password = Column(String, default="")
    voice = Column(String, default="")
    gender = Column(String, default="male")

    def __repr__(self):
        return self.name
