from src.base import *
from flask import request, Response
import time
from src import gen_api


@app.route("/" + API_VERSION + "/pair/<code>/<uuid>/<name>", methods=['PUT'])
@noindex
@donation
@requires_admin
def pair(code, uuid, name="unknown"):
    global unpaired_users
    # pair
    result = {"paired": False}
    if uuid in unpaired_users:
        # auto - pair ?
        real_code = unpaired_users[uuid]
        if real_code == code:
            entered_codes[uuid] = code
            unpaired_users.pop(uuid)
            update_device_data(uuid, {"uuid": uuid, "name": name})
            result = {"paired": True}

            # TODO account creation in pairing ?
            account = {
                'user': {"uuid": uuid, "email": ""}}
            update_device_data(uuid, account)

    return nice_json(result)


@app.route("/"+API_VERSION+"/auth/token", methods=['GET'])
@noindex
@donation
def token():
    api = request.headers.get('Authorization', '').replace("Bearer ", "")
    data = get_device_data(api, refresh=True)
    if not data:
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to authenticate with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="NOT PAIRED"'})

    uuid = data["uuid"]
    old_refresh = data["refreshToken"]

    # token to refresh expired token
    if old_refresh != api:
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to authenticate with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="BAD REFRESH CODE"'})

    # new tokens to access
    access_token = gen_api()
    new_refresh_token = gen_api()

    result = {"expires_at": time.time() + 72000, "accessToken": access_token,
              "refreshToken": new_refresh_token, "uuid": uuid,
              "name": data.get("name", "unknown_device")}

    update_device_data(uuid, result)

    return nice_json(result)


if __name__ == "__main__":
    global app
    port = 6712
    start(app, port)
