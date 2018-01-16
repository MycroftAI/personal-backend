from backend.base import app, noindex, donation, nice_json, \
    API_VERSION, UNPAIRED_DEVICES, DEVICES, start, requires_auth, mail
from flask import redirect, url_for, request, Response
from backend.backend_utils import geo_locate, generate_code, location_dict
from database import gen_api, model_to_dict
from flask_mail import Message
import time


@app.route("/" + API_VERSION + "/device/<uuid>/location", methods=['GET'])
@noindex
@donation
@requires_auth
def location(uuid):
    device = DEVICES.get_device_by_uuid(uuid)
    if device is None:
        return nice_json({"error": "device not found"})
    if device.location.timezone is None:
        if not request.headers.getlist("X-Forwarded-For"):
            ip = request.remote_addr
        else:
            # TODO http://esd.io/blog/flask-apps-heroku-real-ip-spoofing.html
            ip = request.headers.getlist("X-Forwarded-For")[0]
        DEVICES.add_ip(uuid, ip)
        new_location = geo_locate(ip)
        DEVICES.add_location(uuid, new_location)
        return nice_json(new_location)
    location = device.location
    result = location_dict(location.city, location.region_code,
                           location.country_code,
                           location.country_name, location.region,
                           location.longitude,
                           location.latitude, location.timezone)
    return nice_json(result)


@app.route("/" + API_VERSION + "/device/<uuid>/setting", methods=['GET'])
@noindex
@donation
@requires_auth
def setting(uuid=""):
    device = DEVICES.get_device_by_uuid(uuid)
    if device is not None:
        result = model_to_dict(device.config)

        # format result
        cleans = ["skills_dir", "skills_auto_update"]

        blacklisted = [skill.folder for skill in device.config.skills if
                       skill.blacklisted]
        priority = [skill.folder for skill in device.config.skills if
                    skill.priority]

        result["skills"] = {"directory": device.config.skills_dir,
                            "auto_update": device.config.skills_auto_update,
                            "blacklisted_skills": blacklisted,
                            "priority_skills": priority}

        cleans += ["listener_energy_ratio", "record_wake_words",
                   "record_utterances", "wake_word_upload", "stand_up_word",
                   "wake_word", "listener_sample_rate", "listener_channels",
                    "listener_multiplier", "phoneme_duration"]

        result["listener"] = {
            "sample_rate": result["listener_sample_rate"],
            "channels": result["listener_channels"],
            "record_wake_words": result["record_wake_words"],
            "record_utterances": result["record_utterances"],
            "phoneme_duration": result["phoneme_duration"],
            "wake_word_upload": {"enable": result["wake_word_upload"]},
            "multiplier": result["listener_multiplier"],
            "energy_ratio": result["listener_energy_ratio"],
            "wake_word": result["wake_word"],
            "stand_up_word": result["stand_up_word"]
        }

        result["sounds"] = {}
        for sound in device.config.sounds:
            result["sounds"][sound.name] = sound.path

        result["hotwords"] = {}
        for word in device.config.hotwords:
            result["hotwords"][word.name] = {
                "module": word.module,
                "phonemes": word.phonemes,
                "threshold": word.threshold,
                "lang": word.lang,
                "active": word.active,
                "listen": word.listen,
                "utterance": word.utterance,
                "sound": word.sound
            }
        stt = device.config.stt
        result["stt"] = {"module": stt.name,
                         stt.name: {"uri": stt.uri, "token": stt.token,
                                    "lang": stt.lang, "username":
                                        stt.username,
                                    "password": stt.password}
                         }

        tts = device.config.tts
        result["tts"] = {"module": tts.name,
                         tts.name: {"uri": tts.uri, "token": tts.token,
                                    "lang": tts.lang, "username":
                                        tts.username, "password":
                                        tts.password, "voice": tts.voice,
                                    "gender": tts.gender}}

        for c in cleans:
            result.pop(c)

    else:
        result = {}
    return nice_json(result)


@app.route("/" + API_VERSION + "/device/<uuid>", methods=['PATCH', 'GET'])
@noindex
@donation
@requires_auth
def get_uuid(uuid):
    device = DEVICES.get_device_by_uuid(uuid)
    if device is not None:
        if request.method == 'PATCH':
            result = request.json
            DEVICES.add_device(uuid=uuid, name=result.get("name"),
                               expires_at=result.get("expires_at"),
                               accessToken=result.get("accessToken"),
                               refreshToken=result.get("refreshToken"))

        result = model_to_dict(device)
    else:
        result = {}
    return nice_json(result)


@app.route("/" + API_VERSION + "/device/code", methods=['GET'])
@noindex
@donation
def code():
    uuid = request.args["state"]
    code = generate_code()
    print code
    UNPAIRED_DEVICES[uuid] = code
    result = {"code": code, "uuid": uuid}
    return nice_json(result)


@app.route("/" + API_VERSION + "/device", methods=['GET'])
@noindex
@donation
@requires_auth
def device():
    api = request.headers.get('Authorization', '').replace("Bearer ", "")
    device = DEVICES.get_device_by_token(api)
    if device is not None:
        result = model_to_dict(device)
    else:
        result = {}
    return nice_json(result)


@app.route("/" + API_VERSION + "/device/activate", methods=['POST'])
@noindex
@donation
def activate():
    uuid = request.json["state"]

    # paired?
    device = DEVICES.get_device_by_uuid(uuid)
    if device is None:
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to authenticate with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="NOT PAIRED"'})

    # generate access tokens
    DEVICES.add_device(uuid=uuid,
                       expires_at=time.time() + 72000,
                       accessToken=gen_api(),
                       refreshToken=gen_api())
    result = model_to_dict(device)
    return nice_json(result)


@app.route("/" + API_VERSION + "/device/<uuid>/message", methods=['PUT'])
@noindex
@donation
@requires_auth
def send_mail(uuid=""):
    data = request.json
    # sender is meant to id which skill triggered it and is currently ignored
    user = DEVICES.get_user_by_uuid(uuid)
    if user is not None:
        message = data["body"]
        subject = data["title"]
        msg = Message(recipients=[user.email],
                      body=message,
                      subject=subject)
        mail.send(msg)


@app.route("/" + API_VERSION + "/device/<uuid>/metric/<name>",
           methods=['POST'])
@noindex
@donation
@requires_auth
def metric(uuid="", name=""):
    data = request.json
    print name, data
    device = DEVICES.get_device_by_uuid(uuid)
    if device is None:
        return
    DEVICES.add_metric(name=name, uuid=uuid, data=data)


@app.route("/" + API_VERSION + "/device/<uuid>/subscription", methods=['GET'])
@noindex
@donation
@requires_auth
def subscription_type(uuid=""):
    sub_type = "free"
    device = DEVICES.get_device_by_uuid(uuid)
    if device is not None:
        sub_type = device.subscription
    subscription = {"@type": sub_type}
    return nice_json(subscription)


@app.route("/" + API_VERSION + "/device/<uuid>/voice", methods=['GET'])
@noindex
@donation
@requires_auth
def get_subscriber_voice_url(uuid=""):
    arch = request.args["arch"]
    device = DEVICES.get_device_by_uuid(uuid)
    if device is not None:
        device.arch = arch
        DEVICES.commit()
    return nice_json({"link": ""})


if __name__ == "__main__":
    global app
    port = 6712
    start(app, port)
