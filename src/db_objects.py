from sqlalchemy import *


class User(object):
    def __init__(self, name=None, mail=None, password=None, last_seen=0,
                 api=""):
        self.name = name
        self.mail = mail
        self.password = password
        self.last_seen = last_seen
        self.api_key = api

    def __repr__(self):
        return self.name


class IPAddress(object):
    def __init__(self, address=None):
        self.ip_address = address

    def __repr__(self):
        return self.ip_address


class Device(object):
    def __init__(self, uuid="", name="", expires_at=0, accessToken="",
                 refreshToken=""):
        self.expires_at = expires_at
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.uuid = uuid
        self.device_name = name

    def __repr__(self):
        return self.uuid


class Location(object):
    def __init__(self, city="", region_code="", country_code="",
                 country_name="", region="", longitude=0, latitude=0,
                 timezone=""):
        self.city = city
        self.region_code = region_code
        self.country_code = country_code
        self.country_name = country_name
        self.region = region
        self.lon = longitude
        self.lat = latitude
        self.timezone = timezone

        self.region_data = {"code": self.region_code, "name": self.region, "country": {
            "code": self.country_code, "name": self.country_name}}
        self.city_data = {"code": self.city, "name": self.city, "state": self.region_data,
                     "region": self.region_data}
        self.timezone_data = {"code": self.timezone, "name": self.timezone,
                         "dstOffset": 3600000,
                         "offset": -21600000}
        self.coordinate_data = {"latitude": float(self.lat),
                           "longitude": float(self.lon)}
        self.location_data = {"city": self.city_data, "coordinate": self.coordinate_data,
                         "timezone": self.timezone_data}

    def __repr__(self):
        return self.country_name


class Sounds(object):
    def __init__(self, name="", path=""):
        self.path = path
        self.sound_name = name

    def __repr__(self):
        return self.sound_name


class Skill(object):
    def __init__(self, name="", path="", folder="", github=""):
        self.path = path
        self.skill_name = name
        self.folder = folder
        self.github = github

    def __repr__(self):
        return self.name


class Hotword(object):
    def __init__(self, name="", module="", phonemes="", threshold="",
                 lang="en-US", active=False, listen=True, utterance="",
                 sound=""):
        self.hotword_name = name
        self.module = module
        self.phonemes = phonemes
        self.threshold = threshold
        self.hotword_lang = lang
        self.active = active
        self.listen = listen
        self.utterance = utterance
        self.sound = sound

    def __repr__(self):
        return self.hotword_name


class STT(object):
    def __init__(self, name="", lang="en-US", uri="", token="",
                 username="", password=""):
        self.stt_name = name
        self.stt_lang = lang
        self.stt_uri = uri
        self.stt_token = token
        self.stt_username = username
        self.stt_password = password

    def __repr__(self):
        return self.stt_name


class TTS(object):
    def __init__(self, name="", voice="", gender="male", lang="en-US",
                 uri="", token="", username="", password=""):
        self.tts_name = name
        self.tts_lang = lang
        self.tts_uri = uri
        self.tts_token = token
        self.tts_username = username
        self.tts_password = password
        self.tts_voice = voice
        self.tts_gender = gender

    def __repr__(self):
        return self.tts_name


class Configuration(object):
    def __init__(self, config_id, lang="en-US", system_unit="metric",
                 time_format="full", date_format="DMY", opt_in=False,
                 confirm_listening=True, skills_dir="/opt/mycroft/skills",
                 play_wav_cmd="paplay %1 --stream-name=mycroft-voice",
                 play_mp3_cmd="mpg123 %1", auto_update=False,
                 listener_sample_rate=16000, listener_channels=1,
                 record_wake_words=False, record_utterances=False,
                 phoneme_duration=120, listener_multiplier=1.0,
                 listener_energy_ratio=1.5, wake_word="hey mycroft",
                 stand_up_word="wake up", wake_word_upload=False):
        self.config_id = config_id
        self.lang = lang
        self.system_unit = system_unit
        self.time_format = time_format
        self.date_format = date_format
        self.opt_in = opt_in
        self.confirm_listening = confirm_listening
        self.play_wav_cmdline = play_wav_cmd
        self.play_mp3_cmdline = play_mp3_cmd
        self.skills_dir = skills_dir
        self.skills_auto_update = auto_update
        self.listener_sample_rate = listener_sample_rate
        self.listener_channels = listener_channels
        self.record_wake_words = record_wake_words
        self.record_utterances = record_utterances
        self.wake_word_upload = wake_word_upload
        self.phoneme_duration = phoneme_duration
        self.listener_multiplier = listener_multiplier
        self.listener_energy_ratio = listener_energy_ratio
        self.wake_word = wake_word
        self.stand_up_word = stand_up_word

    def __repr__(self):
        return self.config_id


class Database(object):
    def __init__(self, path='sqlite:///mycroft.db', debug=True):
        self.db = create_engine(path)
        self.db.echo = debug
        self.metadata = BoundMetaData(self.db)

        self.tts = Table('tts', self.metadata,
                    Column('tts_id', Integer, primary_key=True),
                    Column('tts_name', String),
                    Column('tts_lang', String),
                    Column('tts_uri', String),
                    Column('tts_token', String),
                    Column('tts_username', String),
                    Column('tts_password', String),
                    Column('tts_voice', String),
                    Column('tts_gender', String),
                    )

        self.stt = Table('stt', self.metadata,
                         Column('stt_id', Integer, primary_key=True),
                         Column('stt_name', String),
                         Column('stt_lang', String),
                         Column('stt_uri', String),
                         Column('stt_token', String),
                         Column('stt_username', String),
                         Column('stt_password', String),
        )

        self.hotwords = Table('hotwords', self.metadata,
            Column('hotword_id', Integer, primary_key = True),
            Column('hotword_name', String),
            Column('module', String),
            Column('phonemes', String),
            Column('hotword_lang', String),
            Column('utterance', String),
            Column('sound', String),
            Column('threshold', String),
            Column('active', Boolean),
            Column('listen', Boolean),
        )

        self.installed_skills = Table('installed_skills', self.metadata,
            Column('skill_name', String, primary_key = True),
            Column('path', String),
            Column('folder', String),
            Column('github', String),
        )

        self.priority_skills = Table('priority_skills', self.metadata,
            Column('skill_name', String, primary_key = True),
            Column('path', String),
            Column('folder', String),
            Column('github', String),
        )

        self.blacklisted_skills = Table('blacklisted_skills', self.metadata,
            Column('skill_name', String, primary_key = True),
            Column('path', String),
            Column('folder', String),
            Column('github', String),
        )

        self.locations = Table('locations', self.metadata,
            Column('location_id', Integer, primary_key = True),
            Column('city', String),
            Column('region_code', String),
            Column('country_code', String),
            Column('country_name', String),
            Column('region', String),
            Column('longitude', Integer),
            Column('latitude', Integer),
            Column('imezone', String),
        )

        self.sounds = Table('sounds', self.metadata,
            Column('sound_name', String, primary_key = True),
            Column('path', String),
        )

        self.configs = Table('configs', self.metadata,
            Column('config_id', Integer, primary_key = True),
            Column('lang', String),
            Column('system_unit', String),
            Column('time_format', String),
            Column('date_format', String),
            Column('opt_in', Boolean),
            Column('confirm_listening', Boolean),
            Column('play_wav_cmdline', String),
            Column('play_mp3_cmdline', String),
            Column('skills_dir', String),
            Column('skills_auto_update', Boolean),
            Column('listener_sample_rate', Integer),
            Column('listener_channels', Integer),
            Column('record_wake_words', Boolean),
            Column('record_utterances', Boolean),
            Column('wake_word_upload', Boolean),
            Column('phoneme_duration', Integer),
            Column('listener_multiplier', Float),
            Column('listener_energy_ratio', Float),
            Column('wake_word', String),
            Column('stand_up_word', String),
        )

        self.users = Table('users', self.metadata,
            Column('user_id', String, primary_key = True),
            Column('name', String(40)),
            Column('mail', String),
            Column('password', String),
            Column('api_key', String),
            Column('last_seen', Integer),
        )

        self.ips = Table('ips', self.metadata,
            Column('ip_address', String, primary_key = True),
        )

        self.devices = Table('devices', self.metadata,
            Column('uuid', String, primary_key = True),
            Column('expires_at', Integer),
            Column('device_name', String),
            Column('accessToken', String),
            Column('refreshToken', String),
        )

        # association tables

        device_association = Table('users_devices', self.metadata,
            Column('user_id', Integer, ForeignKey('devices.uuid')),
            Column('uuid', Integer, ForeignKey('users.user_id')),
        )

        user_association = Table('users_ips', self.metadata,
            Column('user_id', Integer, ForeignKey('ips.ip_address')),
            Column('ip_address', Integer, ForeignKey('users.user_id')),
        )

        ip_association = Table('devices_ips', self.metadata,
            Column('uuid', Integer, ForeignKey('ips.ip_address')),
            Column('ip_address', Integer, ForeignKey('devices.uuid')),
        )

        device_location_association = Table('devices_location', self.metadata,
            Column('uuid', Integer, ForeignKey('locations.location_id')),
            Column('location_id', Integer, ForeignKey('devices.uuid')),
        )

        location_association = Table('configs_location', self.metadata,
            Column('config_id', Integer, ForeignKey('locations.location_id')),
            Column('location_id', Integer, ForeignKey('configs.config_id')),
        )

        config_association = Table('devices_config', self.metadata,
            Column('uuid', Integer, ForeignKey('configs.config_id')),
            Column('config_id', Integer, ForeignKey('devices.uuid')),
        )

        sound_association = Table('sounds_config', self.metadata,
            Column('sound_name', Integer, ForeignKey('configs.config_id')),
            Column('config_id', Integer, ForeignKey('sounds.sound_name')),
        )

        hotword_association = Table('hotwords_config', self.metadata,
            Column('config_id', Integer, ForeignKey('hotwords.hotword_id')),
            Column('hotword_id', Integer, ForeignKey('configs.config_id')),
        )

        tts_association = Table('tts_config', self.metadata,
            Column('config_id', Integer, ForeignKey('tts.tts_id')),
            Column('tts_id', Integer, ForeignKey('configs.config_id')),
            )

        stt_association = Table('stt_config', self.metadata,
            Column('config_id', Integer, ForeignKey('stt.stt_id')),
            Column('stt_id', Integer, ForeignKey('configs.config_id')),
            )

        blacklisted_skills_association = Table('blacklisted_skills_config', self.metadata,
            Column('config_id', Integer, ForeignKey('blacklisted_skills.skill_name')),
            Column('skill_name', Integer, ForeignKey('configs.config_id')),
            )

        priority_skills_association = Table('priority_skills_config', self.metadata,
           Column('config_id', Integer, ForeignKey('priority_skills.skill_name')),
           Column('skill_name', Integer, ForeignKey('configs.config_id')),)

        installed_skills_association = Table('devices_installed_skills', self.metadata,
            Column('uuid', Integer, ForeignKey('installed_skills.skill_name')),
            Column('skill_name', Integer, ForeignKey('devices.uuid')),
            )

        # Handy feature: create all the tables with one function call
        self.metadata.create_all()

        # To create a many-to-many relation, specify the association table as
        # the "secondary" keyword parameter to mapper()
        mapper(IPAddress, self.ips)
        mapper(STT, self.stt)
        mapper(TTS, self.tts)
        mapper(Hotword, self.hotwords)
        mapper(Skill, self.installed_skills)
        mapper(Skill, self.priority_skills)
        mapper(Skill, self.blacklisted_skills)
        mapper(Sounds, self.sounds)
        mapper(Location, self.locations)
        mapper(Configuration, self.configs)
        mapper(Device, self.devices, properties={
            'config': relation(Configuration, secondary=config_association,
                              backref='devices'),
            'location': relation(Location, secondary=device_location_association,
                               backref='devices'),
            'ips': relation(IPAddress, secondary=ip_association,
                                 backref='devices'),
            'skills': relation(Skill, secondary=installed_skills_association,
                            backref='devices'),
        })
        mapper(User, self.users, properties={
            'ips': relation(IPAddress, secondary=user_association,
                            backref='user'),
            'devices': relation(Device, secondary=device_association,
                                backref='user'),
        })
        mapper(Configuration, self.configs, properties={
            'hotwords': relation(Hotword, secondary=hotword_association,
                              backref='config'),
            'tts': relation(TTS, secondary=tts_association,
                                 backref='config'),
            'stt': relation(STT, secondary=stt_association,
                                 backref='config'),
            'blacklisted_skills': relation(Skill, secondary=blacklisted_skills_association,
                            backref='config'),
            'priority_skills': relation(Skill, secondary=priority_skills_association,
                            backref='config'),
            'sounds': relation(Sounds, secondary=sound_association,
                            backref='config'),
            'location': relation(Location, secondary=location_association,
                            backref='config'),
        })

        self.session = create_session()

    def get_user_by_name(self, name):
        return self.session.query(User).get_by(name=name)

    def get_user_by_mail(self, mail):
        return self.session.query(User).get_by(mail=mail)

    def get_user_by_api_key(self, api_key):
        return self.session.query(User).get_by(api_key=api_key)

    def get_user_by_device(self, uuid):
        return self.session.query(User).get_by(uuid=uuid)

    def get_user_by_device_name(self, name):
        return self.session.query(User).get_by(device_name=name)

    def get_user_by_ip(self, ip):
        return self.session.query(User).get_by(ip_adress=ip)

    def get_user_by_config(self, config_id):
        return self.session.query(User).get_by(config_id=config_id)

    def get_user_by_wakeword(self, wakeword):
        return self.session.query(User).get_by(wake_word=wakeword)

    def get_user_by_hotword(self, hotword):
        return self.session.query(User).get_by(hotword_name=hotword)

    def get_user_by_lang(self, lang):
        return self.session.query(User).get_by(lang=lang)

    def get_user_by_country(self, country):
        return self.session.query(User).get_by(country=country)

    def get_user_by_city(self, city):
        return self.session.query(User).get_by(city=city)

    def get_user_by_timezone(self, timezone):
        return self.session.query(User).get_by(timezone=timezone)

    def get_device_by_name(self, name):
        return self.session.query(Device).get_by(device_name=name)

    def get_device_by_user(self, name):
        return self.session.query(Device).get_by(name=name)

    def get_device_by_ip(self, ip):
        return self.session.query(Device).get_by(ip_adress=ip)

    def get_device_by_config(self, config_id):
        return self.session.query(Device).get_by(config_id=config_id)

    def get_device_by_wakeword(self, wakeword):
        return self.session.query(Device).get_by(wake_word=wakeword)

    def get_device_by_hotword(self, hotword):
        return self.session.query(Device).get_by(hotword_name=hotword)

    def get_device_by_lang(self, lang):
        return self.session.query(Device).get_by(lang=lang)

    def get_device_by_country(self, country):
        return self.session.query(Device).get_by(country=country)

    def get_device_by_city(self, city):
        return self.session.query(Device).get_by(city=city)

    def get_device_by_timezone(self, timezone):
        return self.session.query(Device).get_by(timezone=timezone)

    def get_config_by_user(self, name):
        return self.session.query(Configuration).get_by(name=name)

    def get_config_by_device(self, uuid):
        return self.session.query(Configuration).get_by(uuid=uuid)

    def get_config_by_device_name(self, name):
        return self.session.query(Configuration).get_by(device_name=name)