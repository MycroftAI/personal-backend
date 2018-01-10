from src.base import *
from flask import request, Response
import time
from src import gen_api


@app.route("/"+API_VERSION+"/auth/token", methods=['GET'])
@noindex
@donation
def token():
    api = request.headers.get('Authorization', '').replace("Bearer ", "")
    data = retrieve_user_data(api, refresh=True)
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

    result = {"expires_at": time.time() + 9999999999999, "accessToken": access_token,
              "refreshToken": new_refresh_token, "uuid": uuid}

    update_paired_user(uuid, result)

    return nice_json(result)


if __name__ == "__main__":
    global app
    port = 6712
    start(app, port)
