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
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text, \
    Table, Float, Unicode, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

from personal_mycroft_backend.database import Base, props, model_to_dict
import json
import time
from os.path import join, expanduser, exists
from os import makedirs

## association tables


user_devices = Table('user_devices', Base.metadata,
                     Column('user_id', ForeignKey('users.id'),
                            primary_key=True),
                     Column('device_id', ForeignKey('devices.uuid'),
                            primary_key=True)
                     )

config_devices = Table('config_devices', Base.metadata,
                       Column('config_id', ForeignKey('configs.id'),
                              primary_key=True),
                       Column('device_id', ForeignKey('devices.uuid'),
                              primary_key=True)
                       )

config_users = Table('config_users', Base.metadata,
                     Column('config_id', ForeignKey('configs.id'),
                            primary_key=True),
                     Column('user_id', ForeignKey('users.id'),
                            primary_key=True)
                     )

ip_devices = Table('ip_devices', Base.metadata,
                   Column('ip_address', ForeignKey('ips.ip_address'),
                          primary_key=True),
                   Column('device_id', ForeignKey('devices.uuid'),
                          primary_key=True)
                   )

ip_users = Table('ip_users', Base.metadata,
                 Column('ip_address', ForeignKey('ips.ip_address'),
                        primary_key=True),
                 Column('user_id', ForeignKey('users.id'), primary_key=True)
                 )

location_devices = Table('location_devices', Base.metadata,
                         Column('location_id', ForeignKey('locations.id'),
                                primary_key=True),
                         Column('device_id', ForeignKey('devices.uuid'),
                                primary_key=True)
                         )

location_users = Table('location_users', Base.metadata,
                       Column('location_id', ForeignKey('locations.id'),
                              primary_key=True),
                       Column('user_id', ForeignKey('users.id'),
                              primary_key=True)
                       )

location_configs = Table('location_configs', Base.metadata,
                         Column('location_id', ForeignKey('locations.id'),
                                primary_key=True),
                         Column('config_id', ForeignKey('configs.id'),
                                primary_key=True)
                         )

skill_devices = Table('skill_devices', Base.metadata,
                      Column('skill_id', ForeignKey('skills.id'),
                             primary_key=True),
                      Column('device_id', ForeignKey('devices.uuid'),
                             primary_key=True)
                      )

skill_info_devices = Table('skill_info_devices', Base.metadata,
                           Column('skill_id', ForeignKey('skillinfo.identifier'),
                                  primary_key=True),
                           Column('device_id', ForeignKey('devices.uuid'),
                                  primary_key=True)
                           )

skill_configs = Table('skill_configs', Base.metadata,
                      Column('skill_id', ForeignKey('skills.id'),
                             primary_key=True),
                      Column('config_id', ForeignKey('configs.id'),
                             primary_key=True)
                      )

metrics_users = Table('metrics_users', Base.metadata,
                      Column('metric_id', Integer, ForeignKey('metrics.id')),
                      Column('user_id', Integer, ForeignKey('users.id'))
                      )

metrics_devices = Table('metrics_devices', Base.metadata,
                        Column('metric_id', Integer, ForeignKey('metrics.id')),
                        Column('device_id', Integer,
                               ForeignKey('devices.uuid'))
                        )

hotword_configs = Table('hotword_configs', Base.metadata,
                        Column('hotword_id', Integer,
                               ForeignKey('hotwords.id')),
                        Column('config_id', Integer, ForeignKey('configs.id'))

                        )

hotword_devices = Table('hotword_devices', Base.metadata,
                        Column('hotword_id', Integer,
                               ForeignKey('hotwords.id')),
                        Column('device_id', Integer,
                               ForeignKey('devices.uuid'))

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


class UnpairedDevice(Base):
    __tablename__ = 'unpaired'
    created_at = Column(String, default=str(time.time()))
    uuid = Column(String, primary_key=True, nullable=False)
    code = Column(String, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(String, default=time.time())
    password = Column(Text)
    confirmed = Column(Boolean, nullable=False, default=False)
    confirmed_on = Column(Integer)
    token = Column(String)
    name = Column(String, default="unknown_user", unique=True)
    mail = Column(String, nullable=False, unique=True)
    last_seen = Column(Integer, default=0)

    devices = relationship("Device", back_populates="user",
                           secondary=user_devices)
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

    ips = relationship("IPAddress",  # order_by="ips.last_seen",
                       back_populates="devices",
                       secondary=ip_devices)

    location = relationship("Location",  # order_by="locations.id",
                            back_populates="device",
                            secondary=location_devices, uselist=False)
    skills = relationship("Skill", back_populates="device",
                          secondary=skill_devices)

    skills_info = relationship("SkillInfo",
                               back_populates="device",
                               secondary=skill_info_devices)

    metrics = relationship("Metric", back_populates="device",
                           secondary=metrics_devices)

    hotwords = relationship("Hotword", back_populates="device",
                            secondary=hotword_devices)

    @property
    def as_dict(self):
        bucket = model_to_dict(self)
        bucket['location'] = model_to_dict(self.location)
        bucket['user'] = model_to_dict(self.user)
        bucket['setting'] = model_to_dict(self.config)
        # TODO: check API definition document
        bucket['user']['uuid'] = self.user.id
        return bucket



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
    device = relationship("Device",  # order_by="devices.last_seen",
                          back_populates="skills",
                          secondary=skill_devices, uselist=False)
    config = relationship("Configuration",
                          back_populates="skills",
                          secondary=skill_configs, uselist=False)

    priority = Column(Boolean, default=False)
    blacklisted = Column(Boolean, default=False)


class SkillInfo(Base):
    __tablename__ = "skillinfo"
    identifier = Column(String, primary_key=True, nullable=False)
    name = Column(String)
    description = Column(String)
    contributor = Column(String)
    display_name = Column(String)
    color = Column(String)
    skill_gid = Column(String)
    icon = Column(String)
    skillMetadata = Column(String)

    device = relationship("Device",  # order_by="devices.last_seen",
                          back_populates="skills_info",
                          secondary=skill_info_devices, uselist=False)

    @property
    def as_dict(self):
        # this is a placeholder
        bucket = {
            'identifier': str(self.identifier),
            'name': str(self.name),
            'description': str(self.description),
            'contributor': str(self.contributor),
            'icon': str(self.icon),
            'display_name': str(self.display_name),
            'color': str(self.color),
            'skill_gid': str(self.skill_gid),
        }
        if self.skillMetadata is not None and len(self.skillMetadata) > 0:
            bucket['skillMetadata'] = json.loads(str(self.skillMetadata))
        return bucket


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

    @property
    def as_dict(self):
        # this is a placeholder
        # TODO generate proper config matching mycroft.conf
        bucket = model_to_dict(self)
        return bucket


class Configuration(Base):
    __tablename__ = "configs"

    id = Column(Integer, primary_key=True, nullable=False)
    device_id = Column(Integer, ForeignKey("devices.uuid"), nullable=False)

    created_at = Column(String, default=time.time())

    device = relationship("Device", back_populates="config",
                          secondary=config_devices, uselist=False)
    user = relationship("User", back_populates="configs",
                        secondary=config_users, uselist=False)
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

    skills_dir = Column(String, default="~/.mycroft/skills")
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

    @property
    def listener_as_dict(self):
        # this is a placeholder
        # TODO generate proper config matching mycroft.conf
        bucket = {
            "wake_word": self.wake_word,
            "stand_up_word": self.stand_up_word,
            "record_wakewords": self.record_wake_words,
            "record_utterances": self.record_utterances,
            "confirm_listening": self.confirm_listening,
            "wake_word_upload": self.wake_word_upload,
            "sample_rate": self.listener_sample_rate,
            "channels": self.listener_channels,
            "energy_ratio": self.listener_energy_ratio,
            "multiplier": self.listener_multiplier
        }
        return bucket

    @property
    def skills_as_dict(self):
        # this is a placeholder
        # TODO generate proper config matching mycroft.conf
        bucket = {
            "directory": self.skills_dir,
            "auto_update": self.skills_auto_update,
            "blacklisted_skills": [s.folder for s in self.skills if
                                   s.blacklisted],
            "priority_skills": [s.folder for s in self.skills if s.priority]
        }
        return bucket

    @property
    def hotwords_as_dict(self):
        # this is a placeholder
        # TODO generate proper config matching mycroft.conf
        return [model_to_dict(h) for h in self.hotwords]

    @property
    def sounds_as_dict(self):
        # this is a placeholder
        # TODO generate proper config matching mycroft.conf
        return [model_to_dict(h) for h in self.sounds]

    @property
    def as_dict(self):
        # this is a placeholder
        # TODO generate proper config matching mycroft.conf
        bucket = {
            "lang": self.lang,
            "opt_in": self.opt_in,
            "system_unit": self.system_unit,
            "time_format": self.time_format,
            "date_format": self.date_format,
            "listener": self.listener_as_dict,
            "skills": self.skills_as_dict,
            "location": self.location.as_dict,
            "tts": self.tts.as_dict,
            "stt": self.stt.as_dict,
            "hotwords": self.hotwords_as_dict,
            "sounds": self.sounds_as_dict
        }
        return bucket


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
    sound = Column(String, default="")
    lang = Column(String, default="en-us")

    device = relationship("Device", back_populates="hotwords",
                          secondary=hotword_devices, uselist=False)
    user = relationship("User", back_populates="hotwords",
                        secondary=hotword_users, uselist=False)
    config = relationship("Configuration", back_populates="hotwords",
                          secondary=hotword_configs, uselist=False)

    @property
    def as_dict(self):
        # this is a placeholder
        # TODO generate proper config matching mycroft.conf
        bucket = model_to_dict(self)
        return bucket


class Sound(Base):
    __tablename__ = "sounds"
    id = Column(Integer, primary_key=True)
    path = Column(String, default="")
    name = Column(String, default="")
    config = relationship("Configuration", back_populates="sounds",
                          secondary=config_sounds, uselist=False)

    @property
    def as_dict(self):
        # this is a placeholder
        # TODO generate proper config matching mycroft.conf
        bucket = model_to_dict(self)
        return bucket


class STT(Base):
    __tablename__ = "stt_engines"
    id = Column(Integer, primary_key=True, nullable=False)
    engine_type = Column(String, default="")
    name = Column(String, default="")
    lang = Column(String, default="en-us")
    uri = Column(String, default="")
    token = Column(String, default="")
    username = Column(String, default="")
    password = Column(String, default="")
    client_key = Column(String, default="")
    client_id = Column(String, default="")
    config = relationship("Configuration", back_populates="stt",
                          secondary=config_stt, uselist=False)

    @property
    def as_dict(self):
        # this is a placeholder
        # TODO generate proper config matching mycroft.conf
        bucket = {"module": self.name}
        self_dict = model_to_dict(self)
        for k in self_dict:
            if k in ["engine_type", "name", "id"]:
                continue
            if self_dict[k]:
                bucket[k] = self_dict[k]
        return bucket


class TTS(Base):
    __tablename__ = "tts_engines"
    id = Column(Integer, primary_key=True, nullable=False)
    engine_type = Column(String, default="")
    name = Column(String, default="")
    lang = Column(String, default="en-us")
    uri = Column(String, default="")
    token = Column(String, default="")
    username = Column(String, default="")
    password = Column(String, default="")
    client_key = Column(String, default="")
    client_id = Column(String, default="")
    voice = Column(String, default="")
    gender = Column(String, default="")
    api_key = Column(String)

    config = relationship("Configuration", back_populates="tts",
                          secondary=config_tts, uselist=False)

    @property
    def as_dict(self):
        # this is a placeholder
        # TODO generate proper config matching mycroft.conf
        bucket = {"module": self.name}
        self_dict = model_to_dict(self)
        for k in self_dict:
            if k in ["engine_type", "name", "id"]:
                continue
            if self_dict[k]:
                bucket[k] = self_dict[k]
        return bucket


class DeviceDatabase(object):
    def __init__(self, path=None, debug=False, session=None):
        if path is None:
            path = join(expanduser("~"), ".mycroft", "personal_backend")
            if not exists(path):
                makedirs(path)
            path = 'sqlite:///' + join(path, 'devices.db')

        self.db = create_engine(path)
        self.db.echo = debug
        if session:
            self.session = session
        else:
            Session = sessionmaker(bind=self.db)
            self.session = Session()
        Base.metadata.create_all(self.db)

    def get_user_by_pairing_code(self, pairing_code):
        return self.session.query(User).filter(
            User.pairing_code == pairing_code).first()

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
        device = self.session.query(Device).filter(Device.accessToken ==
                                                   token).first()
        if not device:
            device = self.session.query(Device).filter(Device.refreshToken ==
                                                       token).first()
        return device

    def get_skill_info_by_id(self, skill_id):
        return self.session.query(SkillInfo).filter(SkillInfo.identifier == skill_id).first()

    def add_location(self, uuid, location_data=None):
        device = self.get_device_by_uuid(uuid)
        if device is None:
            return False
        location_data = location_data or {}
        location = device.location

        properties = props(Location)

        for arg, val in location_data.items():
            if val and val in properties:
                try:
                    setattr(location, arg, val)
                    self.session.commit()
                except Exception as e:
                    print(e)
                except IntegrityError:
                    self.session.rollback()

        return True

    def add_config(self, uuid, config_data):
        device = self.get_device_by_uuid(uuid)
        if device is None:
            return False
        properties = props(Configuration)
        for arg, val in config_data.items():
            if val and val in properties:
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
        if ip not in [IP.ip_address for IP in device.ips]:
            device.ips.append(IPAddress(ip_address=ip))
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

    def add_unpaired_device(self, uuid, code):
        device = UnpairedDevice(uuid=uuid, code=code)
        try:
            self.session.add(device)
        except Exception as e:
            print("ERROR PAIRING DEVICE", e)
            return False
        return self.commit()

    def get_unpaired_by_code(self, code):
        return self.session.query(UnpairedDevice).filter(
            UnpairedDevice.code == code).first()

    def get_unpaired_by_uuid(self, uuid):
        return self.session.query(UnpairedDevice).filter(
            UnpairedDevice.uuid == uuid).first()

    def remove_unpaired(self, uuid):
        device = self.get_unpaired_by_uuid(uuid)
        self.session.delete(device)
        return self.commit()

    def add_device(self, uuid, name=None, expires_at=None, accessToken=None,
                   refreshToken=None, mail=None):

        user = self.get_user_by_mail(mail) or self.get_user_by_uuid(uuid)
        if user is None:
            print("NOT PAIRED")
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

    def add_skill_info(self, uuid, skill_info_data):
        device = self.get_device_by_uuid(uuid)
        if device is None:
            return False
        skill_id = skill_info_data['identifier']
        skill = self.get_skill_info_by_id(str(skill_id))
        if skill is None:
            skill_info = SkillInfo(identifier=str(skill_info_data['identifier']),
                                   name=str(skill_info_data.get('name', u'')),
                                   description=str(skill_info_data.get('description', u'')),
                                   contributor=str(skill_info_data.get('contributor', u'')),
                                   display_name=str(skill_info_data.get('display_name', u'')),
                                   color=str(skill_info_data.get('color', u'')),
                                   skill_gid=str(skill_info_data.get('skill_gid', u'')),
                                   icon=str(skill_info_data.get('icon', u'')),
                                   skillMetadata=str(skill_info_data.get('skillMetadata', u''))
                                   )
            skill_info.device = device
            device.skills_info.append(skill_info)
            self.session.add(skill_info)
        else:
            skill.name = str(skill_info_data.get('name', '')).encode('utf8')
            skill.description = str(skill_info_data.get('description', u''))
            skill.contributor = str(skill_info_data.get('contributor', u''))
            skill.display_name = str(skill_info_data.get('display_name', u''))
            skill.color = str(skill_info_data.get('color', u''))
            skill.skill_gid = str(skill_info_data.get('skill_gid', u''))
            skill.icon = str(skill_info_data.get('icon', u''))
            skill.skillMetadata = str(skill_info_data.get('skillMetadata', u''))
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

    def close(self):
        self.session.close()

    def __enter__(self):
        """ Context handler """
        return self

    def __exit__(self, _type, value, traceback):
        """ Commits changes and Closes the session """
        self.commit()
        self.close()
