from src.base import app, noindex, donation, nice_json, \
    API_VERSION, UNPAIRED_USERS, DEVICES, start, requires_auth, MAIL, \
    PASSWORD, METRICS
from flask import redirect, url_for, request, Response
from src.util import geo_locate, generate_code, location_dict
from src import gen_api
import yagmail
import time


@app.route("/"+API_VERSION+"/device/<uuid>/location", methods=['GET'])
@noindex
@donation
@requires_auth
def location(uuid):
    config = DEVICES.get_config_by_device(uuid)
    location = config.location
    if not location:
        if not request.headers.getlist("X-Forwarded-For"):
            ip = request.remote_addr
        else:
            # TODO http://esd.io/blog/flask-apps-heroku-real-ip-spoofing.html
            ip = request.headers.getlist("X-Forwarded-For")[0]
        new_location = geo_locate(ip)
        DEVICES.add_location(uuid, new_location)
        return nice_json(new_location)
    result = location_dict(location.city, location.region_code,
                    location.country_code,
                  location.country_name, location.region, location.longitude,
                  location.latitude, location.timezone)
    return nice_json(result)


@app.route("/"+API_VERSION+"/device/<uuid>/setting", methods=['GET'])
@noindex
@donation
@requires_auth
def setting(uuid=""):
    device = DEVICES.get_config_by_device(uuid)
    if len(device):
        device = device[0]
        # TODO test
        result = dict(device.config)
    else:
        result = {}
    return nice_json(result)


@app.route("/"+API_VERSION+"/device/<uuid>", methods=['PATCH', 'GET'])
@noindex
@donation
@requires_auth
def get_uuid(uuid):
    device = DEVICES.get_device_by_uuid(uuid)
    if len(device):
        if request.method == 'PATCH':
            result = request.json
            for key in result:
                try:
                    device[key] = result[key]
                except Exception as e:
                    print e

        device = device[0]
        result = {"expires_at": device.expires_at,
                  "accessToken": device.access_token,
                  "refreshToken": device.refresh_token, "uuid": device.uuid,
                  "name": device.device_name}
    else:
        result = {}
    return nice_json(result)


@app.route("/"+API_VERSION+"/device/code", methods=['GET'])
@noindex
@donation
def code():
    uuid = request.args["state"]
    code = generate_code()
    print code
    UNPAIRED_USERS[uuid] = code
    result = {"code": code, "uuid": uuid}
    return nice_json(result)


@app.route("/"+API_VERSION+"/device", methods=['GET'])
@noindex
@donation
@requires_auth
def device():
    api = request.headers.get('Authorization', '').replace("Bearer ", "")
    device = DEVICES.get_device_by_token(api)
    if len(device):
        device = device[0]
        result = {"expires_at": device.expires_at,
                  "accessToken": device.access_token,
                  "refreshToken": device.refresh_token, "uuid": device.uuid,
                  "name": device.device_name}
    else:
        result = {}
    return nice_json(result)


@app.route("/"+API_VERSION+"/device/activate", methods=['POST'])
@noindex
@donation
def activate():
    uuid = request.json["state"]

    # paired?
    device = DEVICES.get_device_by_uuid(uuid)
    if not len(device):
        return Response(
        'Could not verify your access level for that URL.\n'
        'You have to authenticate with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="NOT PAIRED"'})
    else:
        # should not happen but lets fail safe
        if not DEVICES.is_paired(uuid):
            return Response(
                'Could not verify your access level for that URL.\n'
                'You have to authenticate with proper credentials', 401,
                {'WWW-Authenticate': 'Basic realm="NOT PAIRED"'})
        device = DEVICES.get_device_by_uuid(uuid)[0]

    # generate access tokens
    device.expires_at = time.time() + 72000
    device.accessToken = gen_api()
    device.refreshToken = gen_api()
    device.paired = True
    result = {"expires_at": device.expires_at, "accessToken": device.access_token,
              "refreshToken": device.refresh_token, "uuid": uuid,
              "name": device.device_name, "paired": device.paired}
    return nice_json(result)


@app.route("/"+API_VERSION+"/device/<uuid>/message", methods=['PUT'])
@noindex
@donation
@requires_auth
def send_mail(uuid=""):
    data = request.json
    # sender is meant to id which skill triggered it and is currently ignored
    user = DEVICES.get_user_by_uuid(uuid)
    if len(user):
        user = user[0]
        with yagmail.SMTP(MAIL, PASSWORD) as yag:
            yag.send(user.mail, data["title"], data["body"])


@app.route("/"+API_VERSION+"/device/<uuid>/metric/<name>", methods=['POST'])
@noindex
@donation
@requires_auth
def metric(uuid="", name=""):
    data = request.json
    print name, data
    device = DEVICES.get_device_by_uuid(uuid)
    if not len(device):
        return
    DEVICES.add_metric(name=name, uuid=uuid, data=data)


@app.route("/"+API_VERSION+"/device/<uuid>/subscription", methods=['GET'])
@noindex
@donation
@requires_auth
def subscription_type(uuid=""):
    sub_type = "free"
    device = DEVICES.get_device_by_uuid(uuid)
    if len(device):
        device = device[0]
        sub_type = device.subscription
    subscription = {"@type": sub_type}
    return nice_json(subscription)


@app.route("/"+API_VERSION+"/device/<uuid>/voice", methods=['GET'])
@noindex
@donation
@requires_auth
def get_subscriber_voice_url(uuid=""):
    arch = request.args["arch"]
    device = DEVICES.get_device_by_uuid(uuid)
    if len(device):
        device = device[0]
        device.arch = arch
        DEVICES.commit()
    return nice_json({"link": ""})

if __name__ == "__main__":
    global app
    port = 6712
    start(app, port)
