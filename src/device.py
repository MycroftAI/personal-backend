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


@app.route("/"+API_VERSION+"/device/<uuid>", methods=['PATCH', 'GET'])
@noindex
@donation
@requires_auth
def uuid(uuid):
    if request.method == 'PATCH':
        result = request.json
        update_user_settings(uuid, result)
    result = get_user_settings(uuid)
    return nice_json(result)


@app.route("/"+API_VERSION+"/device/code", methods=['GET'])
@noindex
@donation
def code():
    uuid = request.args["state"]
    code = generate_code()
    print code
    unpaired_users[uuid] = code
    result = {"code": code, "uuid": uuid}
    return nice_json(result)


@app.route("/"+API_VERSION+"/device", methods=['GET'])
@noindex
@donation
@requires_auth
def device():
    api = request.headers.get('Authorization', '').replace("Bearer ", "")
    result = retrieve_user_data(api) or {}
    return nice_json(result)


@app.route("/"+API_VERSION+"/device/activate", methods=['POST'])
@noindex
@donation
def activate():
    uuid = request.json["state"]

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


@app.route("/"+API_VERSION+"/device/<uuid>/message", methods=['PUT'])
@noindex
@donation
@requires_auth
def send_mail(uuid=""):
    data = request.json
    # sender is meant to id which skill triggered it and is currently ignored
    import yagmail
    user_email = retrieve_user_data(uuid=uuid)
    with yagmail.SMTP(MAIL, PASSWORD) as yag:
        yag.send(user_email, data["title"], data["body"])


@app.route("/"+API_VERSION+"/device/<uuid>/metric/<name>", methods=['PUT'])
@noindex
@donation
@requires_auth
def metric(uuid="", name=""):
    data = request.json
    print name, data
    user_data = retrieve_user_data(uuid=uuid)
    if "metrics" not in user_data:
        user_data["metrics"] = {}
    if name not in user_data["metrics"]:
        user_data["metrics"][name] = []
    user_data["metrics"][name].append(data)
    update_user_settings(uuid, data)


if __name__ == "__main__":
    global app
    port = 6712
    start(app, port)
