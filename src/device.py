from src.base import *
from flask import redirect, url_for, request, Response
from src.util import geo_locate, generate_code
from src import gen_api


@app.route("/"+API_VERSION+"/device/<uuid>/location", methods=['GET'])
@noindex
@donation
@requires_auth
def location(uuid):
    result = get_user_settings(uuid).get("location")
    if not result:
        if not request.headers.getlist("X-Forwarded-For"):
            ip = request.remote_addr
        else:
            # TODO http://esd.io/blog/flask-apps-heroku-real-ip-spoofing.html
            ip = request.headers.getlist("X-Forwarded-For")[0]
        result = geo_locate(ip)
        update_user_settings(uuid, {"location": result})
    return nice_json(result)


@app.route("/"+API_VERSION+"/device/<uuid>/setting", methods=['GET'])
@noindex
@donation
@requires_auth
def setting(uuid=""):
    result = get_user_settings(uuid)
    return nice_json(result)


@app.route("/"+API_VERSION+"/device//setting", methods=['GET'])
@noindex
@donation
@requires_auth
def config_not_paired():
    return redirect(url_for(API_VERSION+"/auth/token"), code=302)


@app.route("/"+API_VERSION+"/device/<uuid>", methods=['PATCH'])
@noindex
@donation
@requires_auth
def uuid(uuid):
    result = get_user_settings(uuid)
    print request.json()
    return nice_json(result)


@app.route("/"+API_VERSION+"/device/code", methods=['GET'])
@noindex
@donation
def code():
    uuid = request.args["state"]
    code = generate_code()
    unpaired_users[uuid] = code
    result = {"code": code, "uuid": uuid}
    return nice_json(result)


@app.route("/"+API_VERSION+"/device", methods=['GET'])
@noindex
@donation
def device():
    result = get_user_settings(uuid)
    return nice_json(result)


@app.route("/" + API_VERSION + "/pair/<code>/<uuid>", methods=['PUT'])
@noindex
@donation
@requires_admin
def pair(code, uuid):
    global unpaired_users
    # pair
    result = {"paired": False}
    if uuid in unpaired_users:
        # auto - pair ?
        real_code = unpaired_users[uuid]
        if real_code == code:
            entered_codes[uuid] = code
            unpaired_users.pop(uuid)
            result = {"paired": True}
    return nice_json(result)


@app.route("/"+API_VERSION+"/device/activate", methods=['POST'])
@noindex
@donation
def activate():
    uuid = request.json["state"]
    print "activate", request.json

    # paired?
    if uuid not in entered_codes:
        return Response(
        'Could not verify your access level for that URL.\n'
        'You have to authenticate with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="NOT PAIRED"'})

    #  new tokens to access
    access_token = gen_api()
    new_refresh_token = gen_api()

    result = {"expires_at": time.time() + 9999999999999, "accessToken": access_token,
              "refreshToken": new_refresh_token, "uuid": uuid}
    update_paired_user(uuid, result)
    return nice_json(result)


if __name__ == "__main__":
    global app
    port = 6712
    start(app, port)
