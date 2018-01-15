import time

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text, \
    Table, Float, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#from database.magic import MagicBase as Base


## association tables


user_devices = Table('user_devices', Base.metadata,
     Column('user_id', ForeignKey('users.id'), primary_key=True),
     Column('device_id', ForeignKey('devices.uuid'), primary_key=True)
)


config_devices = Table('config_devices', Base.metadata,
     Column('config_id', ForeignKey('configs.id'), primary_key=True),
     Column('device_id', ForeignKey('devices.uuid'), primary_key=True)
)


config_users = Table('config_users', Base.metadata,
     Column('config_id', ForeignKey('configs.id'), primary_key=True),
     Column('user_id', ForeignKey('users.id'), primary_key=True)
)


ip_devices = Table('ip_devices', Base.metadata,
     Column('ip_address', ForeignKey('ips.ip_address'), primary_key=True),
     Column('device_id', ForeignKey('devices.uuid'), primary_key=True)
)


ip_users = Table('ip_users', Base.metadata,
     Column('ip_address', ForeignKey('ips.ip_address'), primary_key=True),
     Column('user_id', ForeignKey('users.id'), primary_key=True)
)


location_devices = Table('location_devices', Base.metadata,
     Column('location_id', ForeignKey('locations.id'), primary_key=True),
     Column('device_id', ForeignKey('devices.uuid'), primary_key=True)
)


location_users = Table('location_users', Base.metadata,
     Column('location_id', ForeignKey('locations.id'), primary_key=True),
     Column('user_id', ForeignKey('users.id'), primary_key=True)
)


location_configs = Table('location_configs', Base.metadata,
     Column('location_id', ForeignKey('locations.id'),  primary_key=True),
     Column('config_id', ForeignKey('configs.id'), primary_key=True)
)


skill_devices = Table('skill_devices', Base.metadata,
     Column('skill_id', ForeignKey('skills.id'), primary_key=True),
     Column('device_id', ForeignKey('devices.uuid'), primary_key=True)
)


skill_configs = Table('skill_configs', Base.metadata,
     Column('skill_id', ForeignKey('skills.id'), primary_key=True),
     Column('config_id', ForeignKey('configs.id'), primary_key=True)
)


metrics_users = Table('metrics_users', Base.metadata,
    Column('metric_id', Integer, ForeignKey('metrics.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

metrics_devices = Table('metrics_devices', Base.metadata,
    Column('metric_id', Integer, ForeignKey('metrics.id')),
    Column('device_id', Integer, ForeignKey('devices.uuid'))
)

hotword_configs = Table('hotword_configs', Base.metadata,
   Column('hotword_id', Integer, ForeignKey('hotwords.id')),
   Column('config_id', Integer, ForeignKey('configs.id'))

   )

hotword_devices = Table('hotword_devices', Base.metadata,
   Column('hotword_id', Integer, ForeignKey('hotwords.id')),
   Column('device_id', Integer, ForeignKey('devices.uuid'))

   )

hotword_users = Table('hotword_users', Base.metadata,
   Column('hotword_id', Integer, ForeignKey('hotwords.id')),
   Column('user_id', Integer, ForeignKey('users.id'))

   )

config_stt = Table('config_stt', Base.metadata,
    Column('config_id', Integer, ForeignKey('configs.id')),
    Column('stt_id', Integer, ForeignKey('stt_engines.id'))
)

config_tts = Table('config_tts', Base.metadata,
    Column('config_id', Integer, ForeignKey('configs.id')),
    Column('tts_id', Integer, ForeignKey('tts_engines.id'))
)

config_sounds = Table('config_sounds', Base.metadata,
    Column('config_id', Integer, ForeignKey('configs.id')),
    Column('sound_id', Integer, ForeignKey('sounds.id'))
)

# classes


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(String, default=time.time())
    password = Column(Text)
    pairing_code = Column(String)
    name = Column(String, default="unknown_user")
    mail = Column(String, nullable=False, unique=True)
    last_seen = Column(Integer, default=0)

    devices = relationship("Device", back_populates="user", secondary=user_devices)
    configs = relationship("Configuration", back_populates="user",
                         secondary=config_users)
    ips = relationship("IPAddress", back_populates="users",
                           secondary=ip_users)
    locations = relationship("Location", back_populates="user",
                       secondary=location_users)
    metrics = relationship("Metric", back_populates="user",
                           secondary=metrics_users)
    hotwords = relationship("Hotword", back_populates="user",
                            secondary=hotword_users)


class Device(Base):
    __tablename__ = "devices"

    uuid = Column(String, primary_key=True, nullable=False)
    created_at = Column(String, default=time.time())
    description = Column(Text, default="")
    name = Column(String, default="unknown_device")
    last_seen = Column(Integer, default=0)
    expires_at = Column(Integer, default=0)
    accessToken = Column(String)
    refreshToken = Column(String)
    paired = Column(Boolean, default=False)
    subscription = Column(String, default="free")
    arch = Column(String, default="unknown")

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="devices",
                        secondary=user_devices, uselist=False)

    config = relationship("Configuration", back_populates="device",
                           secondary=config_devices, uselist=False)

    ips = relationship("IPAddress", # order_by="ips.last_seen",
                       back_populates="devices",
                       secondary=ip_devices)

    location = relationship("Location",  # order_by="locations.id",
                            back_populates="device",
                            secondary=location_devices, uselist=False)
    skills = relationship("Skill", back_populates="device",
                          secondary=skill_devices)

    metrics = relationship("Metric", back_populates="device",
                           secondary=metrics_devices)

    hotwords = relationship("Hotword", back_populates="device",
                            secondary=hotword_devices)


class Metric(Base):
    __tablename__ = "metrics"
    created_at = Column(Integer, default=time.time())
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)

    system = Column(String)
    start_time = Column(Integer)
    time = Column(Integer)
    intent_type = Column(String)
    lang = Column(String, default="en-us")
    utterance = Column(String)
    handler = Column(String)
    transcription = Column(String)
    source = Column(String)

    device = relationship("Device", back_populates="metrics",
                           secondary=metrics_devices)
    user = relationship("User", back_populates="metrics",
                         secondary=metrics_users)


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(Integer, default=time.time())
    path = Column(String)
    name = Column(String)
    folder = Column(String)
    github = Column(String)
    device = relationship("Device", #order_by="devices.last_seen",
                           back_populates="skills",
                           secondary=skill_devices, uselist=False)
    config = relationship("Configuration",
                          back_populates="skills",
                          secondary=skill_configs, uselist=False)

    priority = Column(Boolean, default=False)
    blacklisted = Column(Boolean, default=False)


class IPAddress(Base):
    __tablename__ = "ips"
    created_at = Column(Integer, default=time.time())
    ip_address = Column(String, primary_key=True, nullable=False)
    last_seen = Column(Integer, default=0)

    users = relationship("User",  # order_by="users.last_seen",
                         back_populates="ips", secondary=ip_users)
    devices = relationship("Device",  # order_by="devices.last_seen",
                           back_populates="ips", secondary=ip_devices)

    def __repr__(self):
        return self.ip_address


class Location(Base):
    __tablename__ = "locations"
    created_at = Column(Integer, default=time.time())
    id = Column(Integer, primary_key=True, nullable=False)
    last_seen = Column(Integer, default=1)
    city = Column(String)
    region_code = Column(String)
    country_code = Column(String)
    country_name = Column(String)
    region = Column(String)
    longitude = Column(Integer, default=0)
    latitude = Column(Integer, default=0)
    timezone = Column(String)

    user = relationship("User",
                         back_populates="locations", uselist=False,
                         secondary=location_users)
    device = relationship("Device",
                           back_populates="location",
                           secondary=location_devices, uselist=False)
    config = relationship("Configuration",
                          back_populates="location",
                          secondary=location_configs, uselist=False)


class Configuration(Base):
    __tablename__ = "configs"

    id = Column(Integer, primary_key=True, nullable=False)
    device_id = Column(Integer, ForeignKey("devices.uuid"), nullable=False)

    created_at = Column(String, default=time.time())

    device = relationship("Device", back_populates="config",
                           secondary=config_devices, uselist=False)
    user = relationship("User", back_populates="configs", secondary=config_users, uselist=False)
    location = relationship("Location", back_populates="config",
                            secondary=location_configs, uselist=False)
    skills = relationship("Skill", back_populates="config",
                          secondary=skill_configs)
    hotwords = relationship("Hotword", back_populates="config",
                            secondary=hotword_configs)
    sounds = relationship("Sound", back_populates="config",
                          secondary=config_sounds)
    stt = relationship("STT", back_populates="config",
                       secondary=config_stt, uselist=False)
    tts = relationship("TTS", back_populates="config",
                       secondary=config_tts, uselist=False)

    lang = Column(String, default="en-us")
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


class Hotword(Base):
    __tablename__ = "hotwords"
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, default="hey mycroft")
    module = Column(String, default="pocketsphinx")
    phonemes = Column(String, default="HH EY . M AY K R AO F T")
    threshold = Column(String, default="1e-90")
    active = Column(Boolean, default=True)
    listen = Column(Boolean, default=False)
    utterance = Column(String, default="")
    sound =Column(String, default="")
    lang = Column(String, default="en-us")

    device = relationship("Device", back_populates="hotwords",
                          secondary=hotword_devices, uselist=False)
    user = relationship("User", back_populates="hotwords",
                        secondary=hotword_users, uselist=False)
    config = relationship("Configuration", back_populates="hotwords",
                        secondary=hotword_configs, uselist=False)


class Sound(Base):
    __tablename__ = "sounds"
    id = Column(Integer, primary_key=True)
    path = Column(String, default="")
    name = Column(String, default="")
    config = relationship("Configuration", back_populates="sounds",
                          secondary=config_sounds, uselist=False)


class STT(Base):
    __tablename__ = "stt_engines"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, default="")
    lang = Column(String, default="en-us")
    uri = Column(String, default="")
    token = Column(String, default="")
    username = Column(String, default="")
    password = Column(String, default="")
    config = relationship("Configuration", back_populates="stt",
                          secondary=config_stt, uselist=False)


class TTS(Base):
    __tablename__ = "tts_engines"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, default="")
    lang = Column(String, default="en-us")
    uri = Column(String, default="")
    token = Column(String, default="")
    username = Column(String, default="")
    password = Column(String, default="")
    voice = Column(String, default="")
    gender = Column(String, default="male")

    config = relationship("Configuration", back_populates="tts",
                          secondary=config_tts, uselist=False)


class DeviceDatabase(object):
    def __init__(self, path='sqlite:///mycroft.db', debug=False):
        self.db = create_engine(path)
        self.db.echo = debug
        Session = sessionmaker(bind=self.db)
        self.session = Session()
        Base.metadata.create_all(self.db)

    def get_user_by_pairing_code(self, pairing_code):
        return self.session.query(User).filter(User.pairing_code == pairing_code).first()

    def get_user_by_id(self, user_id):
        return self.session.query(User).filter(User.id == user_id).first()

    def get_user_by_mail(self, mail):
        return self.session.query(User).filter(User.mail == mail).first()

    def get_user_by_uuid(self, uuid):
        device = self.session.query(Device).filter(Device.uuid ==
                                                   uuid).first()
        if device is not None:
            return device.user

    def get_device_by_uuid(self, uuid):
        return self.session.query(Device).filter(Device.uuid == uuid).first()

    def get_device_by_token(self, token):
        return self.session.query(Device).filter(Device.accessToken ==
                                                 token).first() or \
               self.session.query(Device).filter(Device.refreshToken ==
                                                 token).first()

    def add_location(self, uuid, location_data=None):
        device = self.get_device_by_uuid(uuid)
        if device is None:
            return False
        location_data = location_data or {}
        for arg, val in location_data.items():
            if val:
                try:
                    setattr(device.location, arg, val)
                    self.session.commit()
                except Exception as e:
                    pass
                except IntegrityError:
                    self.session.rollback()

        return True

    def add_config(self, uuid, config_data):
        device = self.get_device_by_uuid(uuid)
        if device is None:
            return False
        for arg, val in config_data.items():
            if val:
                try:
                    setattr(device.config, arg, val)
                    self.session.commit()
                except Exception as e:
                    pass
                except IntegrityError:
                    self.session.rollback()

        return True

    def add_ip(self, uuid, ip):
        device = self.get_device_by_uuid(uuid)
        if device is None:
            return False
        if ip not in [ip.ip_address for ip in device.ips]:
            device.ips.append(IPAddress(ip_address=ip))
        if ip not in [ip.ip_address for ip in device.user.ips]:
            device.user.ips.append(ip)
        return self.commit()

    def add_user(self, mail=None, name="", password=""):
        user = self.session.query(User).filter(User.mail == mail).first()
        if user is None:
            user_id = self.total_users() + 1
            user = User(name=name, mail=mail, password=password, id=user_id)
            self.session.add(user)
        else:
            if mail:
                user.mail = mail
            if name:
                user.name = name
            if password:
                user.password = password
        return self.commit()

    def add_device(self, uuid, name=None,
                   expires_at=None,
                   accessToken=None,
                   refreshToken=None, mail=None):

        user = self.get_user_by_mail(mail) or self.get_user_by_uuid(uuid)
        if user is None:
            print "NOT PAIRED"
            return False

        device = self.get_device_by_uuid(uuid)
        if device is None:
            device = Device(uuid=uuid, user_id=user.id, user=user, paired=True)
            # create default configuration
            config = Configuration(id=self.total_configs() + 1,
                                   device_id=device.uuid, user=user)

            # add location entry to config
            location = Location(
                id=self.session.query(Configuration).count() + 1,
                device=device, user=user)
            config.location = location

            # add default STT and TTS engines to config
            config.stt = STT(id=self.session.query(STT).count() + 1,
                             name="mycroft")
            config.tts = TTS(id=self.session.query(TTS).count() + 1,
                             name="mimic")

            # add default hey mycroft hotword to config
            hotword = Hotword(id=self.session.query(Hotword).count() + 1,
                              device=device,
                              user=user)
            wakeword = Hotword(id=self.session.query(Hotword).count() + 1,
                              device=device,
                              user=user, phonemes="W EY K . AH P",
                               threshold="1e-20", name="wake up")
            config.hotwords.append(hotword)
            config.hotwords.append(wakeword)

            # add default priority skills
            config.skills.append(
                Skill(id=self.session.query(Skill).count() + 1,
                      name="pairing", folder="skill-pairing",
                      priority=True, device=device))

            # add default blacklisted skills
            config.skills.append(
                Skill(id=self.session.query(Skill).count() + 1,
                      name="skill-media", folder="skill-media",
                      blacklisted=True, device=device))
            config.skills.append(
                Skill(id=self.session.query(Skill).count() + 1,
                      name="send-sms", folder="send-sms",
                      blacklisted=True, device=device))
            config.skills.append(
                Skill(id=self.session.query(Skill).count() + 1,
                      name="skill-wolfram-alpha",
                      folder="skill-wolfram-alpha",
                      blacklisted=True, device=device))

            # add default sounds
            config.sounds.append(
                Sound(id=self.session.query(Sound).count() + 1,
                      name="start_listening",
                      path="snd/start_listening.wav", ))
            config.sounds.append(
                Sound(id=self.session.query(Sound).count() + 1,
                      name="end_listening",
                      path="snd/end_listening.wav", ))
            # add config to device
            device.config = config
            self.session.add(device)

        if name:
            device.name = name
        if expires_at:
            device.expires_at = expires_at
        if accessToken:
            device.accessToken = accessToken
        if refreshToken:
            device.refreshToken = refreshToken

        return self.commit()

    def total_users(self):
        return self.session.query(User).count()

    def total_devices(self):
        return self.session.query(Device).count()

    def total_configs(self):
        return self.session.query(Configuration).count()

    def commit(self):
        try:
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
        return False