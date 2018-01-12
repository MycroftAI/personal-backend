from sqlalchemy import Column, Text, String, Integer, create_engine, \
    ForeignKey, Boolean, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

from database import Base

import time


device_user = Table('device_user', Base.metadata,
    Column('uuid', Integer, ForeignKey('devices.uuid')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


device_ips = Table('device_ips', Base.metadata,
    Column('uuid', Integer, ForeignKey('devices.uuid')),
    Column('ip_addresses', Integer, ForeignKey('ips.ip_address'))
)


device_location = Table('device_location', Base.metadata,
    Column('uuid', Integer, ForeignKey('devices.uuid')),
    Column('location_id', Integer, ForeignKey('locations.id'))
)


device_metrics = Table('device_metrics', Base.metadata,
    Column('uuid', Integer, ForeignKey('devices.uuid')),
    Column('metrics_id', Integer, ForeignKey('metric.id'))
)


device_config = Table('device_config', Base.metadata,
    Column('uuid', Integer, ForeignKey('devices.uuid')),
    Column('config_id', Integer, ForeignKey('configs.uuid'))
)

device_skills = Table('device_skills', Base.metadata,
    Column('uuid', Integer, ForeignKey('devices.uuid')),
    Column('skill_names', Integer, ForeignKey('skills.name'))
)


device_hotwords = Table('device_hotwords', Base.metadata,
    Column('uuid', Integer, ForeignKey('devices.uuid')),
    Column('hotword_names', Integer, ForeignKey('hotwords.name'))
)

ip_users = Table('ip_users', Base.metadata,
    Column('ip_address', Integer, ForeignKey('ips.ip_address')),
    Column('user_ids', Integer, ForeignKey('users.id'))
)

ip_devices = Table('ip_devices', Base.metadata,
    Column('ip_address', Integer, ForeignKey('ips.ip_address')),
    Column('devices', Integer, ForeignKey('devices.uuid'))
)


location_users = Table('location_users', Base.metadata,
    Column('location', Integer, ForeignKey('locations.id')),
    Column('user_ids', Integer, ForeignKey('users.id'))
)

location_devices = Table('location_devices', Base.metadata,
    Column('location', Integer, ForeignKey('locations.id')),
    Column('uuids', Integer, ForeignKey('devices.uuid'))
)

skill_devices = Table('skill_devices', Base.metadata,
    Column('skill_name', Integer, ForeignKey('skills.name')),
    Column('uuids', Integer, ForeignKey('devices.uuid'))
)


class Device(Base):
    __tablename__ = "devices"
    created_at = Column(Integer, default=time.time())
    uuid = Column(Text, primary_key=True)
    description = Column(Text)
    name = Column(String, default="unknown_device")
    last_seen = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("User.id"))
    ip_addresses = Column(String, ForeignKey("IPAddress.ip_address"))
    location_id = Column(String, ForeignKey("Location.uuid"))
    metrics_id = Column(String, ForeignKey("Metrics.uuid"))
    skill_names = Column(String, ForeignKey("Skill.name"))
    hotword_names = Column(String, ForeignKey("Hotword.name"))

    user = relationship("User", order_by="User.id",
                        back_populates="devices",
                           secondary=device_user)
    ips = relationship("IPAddress", order_by="IPAddress.last_seen",
                       back_populates="devices",
                           secondary=device_ips)
    location = relationship("Location", order_by="Location.id",
                            back_populates="devices",
                           secondary=device_location)
    skills = relationship("Skill", back_populates="devices",
                           secondary=device_skills)
    metrics = relationship("Metric", back_populates="users",
                           secondary=device_metrics)
    config = relationship("Configuration", back_populates="device",
                           secondary=device_config)
    hotwords = relationship("Hotword", back_populates="devices",
                           secondary=device_hotwords)

    expires_at = Column(Integer, default=0)
    accessToken = Column(String)
    refreshToken = Column(String)
    paired = Column(Boolean, default=False)
    subscription = Column(String, default="free")
    arch = Column(String, default="unknown")

    def __repr__(self):
        return self.uuid


class IPAddress(Base):
    __tablename__ = "ips"
    created_at = Column(Integer, default=time.time())
    ip_address = Column(String, primary_key=True)
    last_seen = Column(Integer, default=0)
    uuids = Column(Integer, ForeignKey("Device.uuid"))
    users = relationship("User", order_by="User.last_seen",
                         back_populates="ips",
                           secondary=ip_users)
    devices = relationship("Device", order_by="Device.last_seen",
                           back_populates="ips",
                           secondary=ip_devices)

    def __repr__(self):
        return self.ip_address


class Location(Base):
    __tablename__ = "locations"
    created_at = Column(Integer, default=time.time())
    id = Column(Integer, primary_key=True)
    last_seen = Column(Integer, default=0)
    city = Column(String)
    region_code = Column(String)
    country_code = Column(String)
    country_name = Column(String)
    region = Column(String)
    longitude = Column(Integer, default=0)
    latitude = Column(Integer, default=0)
    timezone = Column(String)
    users = relationship("User", order_by="User.id",
                         back_populates="locations",
                           secondary=location_users)
    devices = relationship("Device", order_by="Device.last_seen",
                           back_populates="location",
                           secondary=location_devices)

    def __repr__(self):
        return self.country_name


class Skill(Base):
    __tablename__ = "skills"
    created_at = Column(Integer, default=time.time())
    path = Column(String)
    name = Column(String)
    folder = Column(String, primary_key=True)
    github = Column(String)
    devices = relationship("Device", order_by="Device.last_seen",
                           back_populates="skills",
                           secondary=skill_devices)
    priority = Column(Boolean, default=False)
    blacklisted = Column(Boolean, default=False)

    def __repr__(self):
        return self.skill_name


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
        return self.session.query("User").count()

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
        return self.session.query("Metric").count()

    def commit(self):
        self.session.commit()

