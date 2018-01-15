from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text, \
    Table, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

import time

Base = declarative_base()


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
    description = Column(Text)
    api_key = Column(String)
    name = Column(String, default="unknown_user")
    mail = Column(String, nullable=False)
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
                        secondary=user_devices, uselist=False, load_on_pending=True)

    config = relationship("Configuration", back_populates="device",
                           secondary=config_devices, uselist=False)

    ips = relationship("IPAddress", # order_by="ips.last_seen",
                       back_populates="devices",
                       secondary=ip_devices)

    location = relationship("Location",  # order_by="locations.id",
                            back_populates="device",
                            secondary=location_devices)
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
    lang = Column(String)
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

    def __repr__(self):
        return self.skill_name


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
    id = Column(Integer, primary_key=True)
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
                       secondary=config_stt)
    tts = relationship("TTS", back_populates="config",
                       secondary=config_tts)

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

    def get_user_by_name(self, name):
        return self.session.query("User").filter_by("User.name" == name).all()

    def get_user_by_mail(self, mail):
        return self.session.query("User").filter_by("User.mail" == mail).all()

    def get_user_by_api_key(self, api_key):
        return self.session.query("User").filter_by("User.api_key"
                                                  == api_key).all()

    def get_user_by_device(self, uuid):
        return self.session.query("User").filter_by(Device.uuid == uuid).all()

    def get_user_by_device_name(self, name):
        return self.session.query("User").filter_by(
            Device.device_name == name).all()

    def get_user_by_ip(self, ip):
        return self.session.query("User").filter_by(IPAddress.ip_address ==
                                                  ip).all()

    def get_user_by_wakeword(self, wakeword):
        return self.session.query("User").filter_by(
            "Configuration.wake_word" == wakeword).all()

    def get_user_by_hotword(self, hotword):
        return self.session.query("User").filter_by("Hotword.name" == hotword)

    def get_user_by_lang(self, lang):
        return self.session.query("User").filter_by(
            "Configuration.lang" == lang).all()

    def get_user_by_country(self, country):
        return self.session.query("User").filter_by(
            Location.country_name == country).all()

    def get_user_by_city(self, city):
        return self.session.query("User").filter_by(Location.city == city).all()

    def get_user_by_timezone(self, timezone):
        return self.session.query("User").filter_by(
            Location.timezone == timezone).all()

    def get_device_by_uuid(self, uuid):
        return self.session.query(Device).filter_by(Device.uuid == uuid).all()

    def get_device_by_name(self, name):
        return self.session.query(Device).filter_by(Device.name == name).all()

    def get_device_by_user(self, name):
        return self.session.query(Device).filter_by("User.name" == name).all()

    def get_device_by_ip(self, ip):
        return self.session.query(Device).filter_by(
            IPAddress.ip_adress == ip).all()

    def get_device_by_wakeword(self, wakeword):
        return self.session.query(Device).filter_by(
            "Configuration.wake_word" == wakeword).all()

    def get_device_by_hotword(self, hotword):
        return self.session.query(Device).filter_by(
            "Hotword.name" == hotword).all()

    def get_device_by_lang(self, lang):
        return self.session.query(Device).filter_by(
            "Configuration.lang" == lang).all()

    def get_device_by_country(self, country):
        return self.session.query(Device).filter_by(
            Location.country == country).all()

    def get_device_by_city(self, city):
        return self.session.query(Device).filter_by(
            Location.city == city).all()

    def get_device_by_token(self, token):
        return self.session.query(Device).filter_by(
            Device.accessToken == token).all()

    def get_device_by_timezone(self, timezone):
        return self.session.query(Device).filter_by(
            Location.timezone == timezone).all()

    def get_config_by_user(self, name):
        return self.session.query("Configuration").filter_by(
           "User.name" == name).all()

    def get_config_by_device(self, uuid):
        return self.session.query("Configuration").filter_by(
            Device.uuid == uuid).one()

    def get_location_by_device(self, uuid):
        return self.session.query(Location).filter_by(
            Device.uuid == uuid).one()

    def get_config_by_device_name(self, name):
        return self.session.query("Configuration").filter_by(
            Device.name == name).all()

    def add_user(self, mail=None, name="", password="", api=""):
        user = User(name=name, mail=mail, password=password, api_key=api)
        try:
            self.session.add(user)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
        return False

    def add_device(self, uuid, name=None, expires_at=None, accessToken=None,
                   refreshToken=None, paired=False):
        device = Device(uuid=uuid)
        if name:
            device.name = name
        if expires_at:
            device.expires_at = expires_at
        if accessToken:
            device.accessToken = accessToken
        if refreshToken:
            device.refreshToken = refreshToken
        if paired:
            device.paired = paired

        try:
            self.session.add(device)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
        return False

    def add_location(self, uuid, data=None):
        data = data or {}
        try:
            location = Location(city=data.get("city", ""),
                                region_code=data.get("region_code", ""),
                                country_code=data.get('country_code', ""),
                                country_name=data.get("country_name", ""),
                                region=data.get("region", ""),
                                longitude=data.get("longitude", 0),
                                latitude=data.get("latitude", 0),
                                timezone=data.get("timezone", ""),
                                id=self.total_locations()+1,
                                uuid=uuid)
            self.session.add(location)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
        return False

    def add_metric(self, uuid, name, data=None):
        data = data or {}
        try:
            metric = Metric(uuid=uuid, id=self.total_metrics() +1, name=name)
            for key in data:
                try:
                    metric[key] = data[key]
                except Exception as e:
                    print e
            self.session.add(metric)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
        return False

    def add_config(self, uuid, data=None):
        data = data or {}
        config = Configuration(uuid=uuid)
        for key in data:
            try:
                config[key] = data[key]
            except Exception as e:
                print e
        try:
            self.session.add(config)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
        return False

    def update_user_timestamp(self, mail, timestamp):
        user = self.get_user_by_mail(mail)
        if user:
            user = user[0]
        else:
            return False
        user.last_seen = timestamp
        self.commit()
        return True

    def update_device_timestamp(self, uuid, timestamp):
        device = self.get_device_by_uuid(uuid)
        if device:
            device = device[0]
        else:
            return False
        device.last_seen = timestamp
        self.commit()
        return True

    def is_paired(self, uuid):
        return self.session.query(Device).filter_by(Device.uuid == uuid)\
            .filter_by(Device.paired == True).all()

    def total_users(self):
        return self.session.query(User).count()

    def total_devices(self):
        return self.session.query(Device).count()

    def total_configs(self):
        return self.session.query("Configuration").count()

    def total_locations(self):
        return self.session.query(Location).count()

    def total_hotwords(self):
        return self.session.query("Hotword").count()

    def total_skills(self):
        return self.session.query(Skill).filter_by(Skill.name).count()

    def total_ips(self):
        return self.session.query(IPAddress).count()

    def total_langs(self):
        return self.session.query("Configuration").filter_by("Configuration.lang").count()

    def total_countries(self):
        return self.session.query("Configuration").filter_by(
            Location.country_code).count()

    def total_stt(self):
        return self.session.query("STT").filter_by("STT.name").count()

    def total_tts(self):
        return self.session.query("TTS").filter_by("TTS.name").count()

    def total_metrics(self):
        return self.session.query(Metric).count()

    def commit(self):
        self.session.commit()

db = DeviceDatabase()
print db.total_metrics()
print db.total_users()
print db.total_devices()