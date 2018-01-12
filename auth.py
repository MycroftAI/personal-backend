from base import app, noindex, donation, requires_admin, nice_json, \
    API_VERSION, UNPAIRED_USERS, DEVICES, start
from flask import request, Response
import time
from . import gen_api


@app.route("/" + API_VERSION + "/pair/<code>/<uuid>/<name>", methods=['PUT'])
@noindex
@donation
@requires_admin
def pair(code, uuid, name="unknown"):
    # pair
    result = {"paired": False}
    if uuid in UNPAIRED_USERS:
        # auto - pair ?
        real_code =UNPAIRED_USERS[uuid]
        if real_code == code:
            UNPAIRED_USERS.pop(uuid)
            DEVICES.add_device(uuid, name, paired=True)
            result = {"paired": True}
    return nice_json(result)


@app.route("/"+API_VERSION+"/auth/token", methods=['GET'])
@noindex
@donation
def token():
    api = request.headers.get('Authorization', '').replace("Bearer ", "")
    device = DEVICES.get_device_by_token(api)
    if not len(device):
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to authenticate with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="NOT PAIRED"'})

    device = device[0]

    # token to refresh expired token
    if device.refreshToken != api:
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to authenticate with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="BAD REFRESH CODE"'})

    # new tokens to access
    access_token = gen_api()
    new_refresh_token = gen_api()

    device.expires_at = time.time() + 72000
    device.accessToken = access_token
    device.refreshToken = new_refresh_token
    DEVICES.commit()

    result = {"expires_at": device.expires_at, "accessToken": access_token,
              "refreshToken": new_refresh_token, "uuid": device.uuid,
              "name": device.device_name}

    return nice_json(result)


if __name__ == "__main__":
    global app
    port = 6712
    start(app, port)
