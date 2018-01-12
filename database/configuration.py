from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Float, Table
from sqlalchemy.orm import relationship

from database import Base


config_users = Table('config_users', Base.metadata,
    Column('config', Integer, ForeignKey('configs.uuid')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

config_devices = Table('config_devices', Base.metadata,
    Column('config', Integer, ForeignKey('configs.uuid')),
    Column('uuid', Integer, ForeignKey('devices.uuid'))
)

config_hotwords = Table('config_hotwords', Base.metadata,
    Column('config', Integer, ForeignKey('configs.uuid')),
    Column('hotwords', Integer, ForeignKey('hotwords.uuid'))
)

config_stt = Table('config_stt', Base.metadata,
    Column('config', Integer, ForeignKey('configs.uuid')),
    Column('stt', Integer, ForeignKey('stt_engines.uuid'))
)

config_tts = Table('config_tts', Base.metadata,
    Column('config', Integer, ForeignKey('configs.uuid')),
    Column('tts', Integer, ForeignKey('tts_engines.uuid'))
)

config_sounds = Table('config_sounds', Base.metadata,
    Column('config', Integer, ForeignKey('configs.uuid')),
    Column('sounds', Integer, ForeignKey('sounds.uuid'))
)

config_skills = Table('config_skills', Base.metadata,
    Column('config', Integer, ForeignKey('configs.uuid')),
    Column('skills', Integer, ForeignKey('skills.uuid'))
)

sound_configs = Table('sound_configs', Base.metadata,
    Column('sounds', Integer, ForeignKey('sounds.uuid')),
    Column('config', Integer, ForeignKey('configs.uuid'))

)

hotword_configs = Table('hotword_configs', Base.metadata,
   Column('hotword_id', Integer, ForeignKey('hotwords.uuid')),
   Column('config', Integer, ForeignKey('configs.uuid'))

   )

hotword_devices = Table('hotword_devices', Base.metadata,
   Column('hotword_id', Integer, ForeignKey('hotwords.uuid')),
   Column('devices', Integer, ForeignKey('devices.uuid'))

   )

hotword_users = Table('hotword_users', Base.metadata,
   Column('hotword_id', Integer, ForeignKey('hotwords.uuid')),
   Column('users', Integer, ForeignKey('users.id'))

   )


stt_configs = Table('stt_configs', Base.metadata,
   Column('stt_id', Integer, ForeignKey('stt_engines.uuid')),
   Column('config', Integer, ForeignKey('configs.uuid'))

   )

tts_configs = Table('tts_configs', Base.metadata,
   Column('tts_id', Integer, ForeignKey('tts_engines.uuid')),
   Column('config', Integer, ForeignKey('configs.uuid'))

   )


class Configuration(Base):
    __tablename__ = "configs"
    uuid = Column(String, ForeignKey("Device.uuid"), primary_key=True)
    device = relationship("Device", back_populates="config",
                           secondary=config_devices)
    users = relationship("User", back_populates="configs",
                           secondary=config_users)
    hotwords = relationship(Hotword, back_populates="configs",
                           secondary=config_hotwords)
    stt = relationship(STT, back_populates="configs",
                           secondary=config_stt)
    tts = relationship(TTS, back_populates="configs",
                           secondary=config_tts)
    sounds = relationship(Sounds, back_populates="configs",
                           secondary=config_sounds)
    skills = relationship("Skill", back_populates="configs",
                           secondary=config_skills)

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
    uuid = Column(String, ForeignKey("Device.uuid"), primary_key=True)
    configs = relationship(Configuration, back_populates="sounds",
                           secondary=sound_configs)
    path = Column(String, default="")
    name = Column(String, default="")

    def __repr__(self):
        return self.name


class Hotword(Base):
    __tablename__ = "hotwords"
    uuid = Column(String, ForeignKey("Device.uuid"), primary_key=True)
    devices = relationship("Device", back_populates="hotwords",
                           secondary=hotword_devices)
    users = relationship("User", back_populates="hotwords",
                           secondary=hotword_users)
    configs = relationship(Configuration, back_populates="hotwords",
                           secondary=hotword_configs)
    name = Column(String, default="wake up")
    module = Column(String, default="pocketsphinx")
    phonemes = Column(String, default="HH EY . M AY K R AO F T")
    threshold = Column(String, default="1e-90")
    active = Column(Boolean, default=False)
    listen = Column(Boolean, default=False)
    utterance = Column(String, default="")
    sound =Column(String, default="")
    lang = Column(String, default="en-us")

    def __repr__(self):
        return self.name


class STT(Base):
    __tablename__ = "stt_engines"
    uuid = Column(String, ForeignKey("Device.uuid"), primary_key=True)
    configs = relationship(Configuration, back_populates="stt",
                           secondary=stt_configs)
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
    uuid = Column(String, ForeignKey("Device.uuid"), primary_key=True)
    configs = relationship(Configuration, back_populates="tts",
                           secondary=tts_configs)
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
