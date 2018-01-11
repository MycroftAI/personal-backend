from sqlalchemy import *


class User(object):
    def __init__(self, name=None, mail=None, password=None, last_seen=0):
        self.name = name
        self.mail = mail
        self.password = password
        self.last_seen = last_seen

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
        self.name = name

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
        self.name = name

    def __repr__(self):
        return self.name


class Skill(object):
    def __init__(self, name="", path="", folder="", github=""):
        self.path = path
        self.name = name
        self.folder = folder
        self.github = github

    def __repr__(self):
        return self.name


class Hotword(object):
    def __init__(self, name="", module="", phonemes="", threshold="",
                 lang="en-US", active=False, listen=True, utterance="",
                 sound=""):
        self.name = name
        self.module = module
        self.phonemes = phonemes
        self.threshold = threshold
        self.lang = lang
        self.active = active
        self.listen = listen
        self.utterance = utterance
        self.sound = sound

    def __repr__(self):
        return self.name


class STT(object):
    def __init__(self, name="", lang="en-US", uri="", token="",
                 username="", password=""):
        self.name = name
        self.lang = lang
        self.uri = uri
        self.token = token
        self.username = username
        self.password = password

    def __repr__(self):
        return self.name


class TTS(object):
    def __init__(self, name="", voice="", gender="male", lang="en-US",
                 uri="", token="", username="", password=""):
        self.name = name
        self.lang = lang
        self.uri = uri
        self.token = token
        self.username = username
        self.password = password
        self.voice = voice
        self.gender = gender

    def __repr__(self):
        return self.name


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
        # TODO table for listening sounds
        self.play_wav_cmdline = play_wav_cmd
        self.play_mp3_cmdline = play_mp3_cmd
        self.skills_dir = skills_dir
        self.skills_auto_update = auto_update
        # TODO table for skills
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
        # TODO hotwords table
        # TODO stt table
        # TODO tts table

    def __repr__(self):
        return self.config_id


class Database(object):
    def __init__(self, path='sqlite:///mycroft.db', debug=True):
        self.db = create_engine(path)
        self.db.echo = debug
        self.metadata = BoundMetaData(self.db)

        tts = Table('tts', self.metadata,
                    Column('tts_id', Integer, primary_key=True),
                    Column('name', String),
                    Column('lang', String),
                    Column('uri', String),
                    Column('token', String),
                    Column('username', String),
                    Column('password', String),
                    Column('voice', String),
                    Column('gender', String),
                    )

        stt = Table('stt', self.metadata,
                         Column('stt_id', Integer, primary_key=True),
                         Column('name', String),
                         Column('lang', String),
                         Column('uri', String),
                         Column('token', String),
                         Column('username', String),
                         Column('password', String),
        )

        hotwords = Table('hotwords', self.metadata,
            Column('hotword_id', Integer, primary_key = True),
            Column('name', String),
            Column('module', String),
            Column('phonemes', String),
            Column('lang', String),
            Column('utterance', String),
            Column('sound', String),
            Column('threshold', String),
            Column('active', Boolean),
            Column('listene', Boolean),
        )

        installed_skills = Table('installed_skills', self.metadata,
            Column('name', String, primary_key = True),
            Column('path', String),
            Column('folder', String),
            Column('github', String),
        )

        priority_skills = Table('priority_skills', self.metadata,
            Column('name', String, primary_key = True),
            Column('path', String),
            Column('folder', String),
            Column('github', String),
        )

        blacklisted_skills = Table('blacklisted_skills', self.metadata,
            Column('name', String, primary_key = True),
            Column('path', String),
            Column('folder', String),
            Column('github', String),
        )

        locations = Table('locations', self.metadata,
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

        sounds = Table('sounds', self.metadata,
            Column('name', String, primary_key = True),
            Column('path', String),
        )

        configs = Table('configs', self.metadata,
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

        users = Table('users', self.metadata,
            Column('user_id', String, primary_key = True),
            Column('name', String(40)),
            Column('mail', String),
            Column('password', String),
            Column('last_seen', Integer),
        )

        ips = Table('ips', self.metadata,
            Column('address', String, primary_key = True),
        )

        devices = Table('devices', self.metadata,
            Column('uuid', String, primary_key = True),
            Column('expires_at', Integer),
            Column('name', String),
            Column('accessToken', String),
            Column('refreshToken', String),
        )

        # association tables

        device_association = Table('users_devices', self.metadata,
            Column('user_id', Integer, ForeignKey('devices.uuid')),
            Column('uuid', Integer, ForeignKey('users.user_id')),
        )

        user_association = Table('users_ips', self.metadata,
            Column('user_id', Integer, ForeignKey('ips.address')),
            Column('address', Integer, ForeignKey('users.user_id')),
        )

        ip_association = Table('devices_ips', self.metadata,
            Column('uuid', Integer, ForeignKey('ips.address')),
            Column('address', Integer, ForeignKey('devices.uuid')),
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
            Column('name', Integer, ForeignKey('configs.config_id')),
            Column('config_id', Integer, ForeignKey('sounds.name')),
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
            Column('config_id', Integer, ForeignKey('blacklisted_skills.name')),
            Column('name', Integer, ForeignKey('configs.config_id')),
            )

        priority_skills_association = Table('priority_skills_config', self.metadata,
           Column('config_id', Integer, ForeignKey('priority_skills.name')),
           Column('name', Integer, ForeignKey('configs.config_id')),)

        installed_skills_association = Table('devices_installed_skills', self.metadata,
            Column('uuid', Integer, ForeignKey('installed_skills.name')),
            Column('name', Integer, ForeignKey('devices.uuid')),
            )

        # Handy feature: create all the tables with one function call
        self.metadata.create_all()

        # To create a many-to-many relation, specify the association table as
        # the "secondary" keyword parameter to mapper()
        mapper(IPAddress, ips)
        mapper(STT, stt)
        mapper(TTS, tts)
        mapper(Hotword, hotwords)
        mapper(Skill, installed_skills)
        mapper(Skill, priority_skills)
        mapper(Skill, blacklisted_skills)
        mapper(Sounds, sounds)
        mapper(Location, locations)
        mapper(Configuration, configs)
        mapper(Device, devices, properties={
            'config': relation(Configuration, secondary=config_association,
                              backref='devices'),
            'location': relation(Location, secondary=device_location_association,
                               backref='devices'),
            'ips': relation(IPAddress, secondary=ip_association,
                                 backref='devices'),
            'skills': relation(Skill, secondary=installed_skills_association,
                            backref='devices'),
        })
        mapper(User, users, properties={
            'ips': relation(IPAddress, secondary=user_association,
                            backref='user'),
            'devices': relation(Device, secondary=device_association,
                                backref='user'),
        })
        mapper(Configuration, config, properties={
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