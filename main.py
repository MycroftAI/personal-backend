from base import app, start
from device import location, setting, get_uuid, code, device, activate,\
    send_mail, metric, subscription_type, get_subscriber_voice_url
from auth import pair, token
from stt import stt
from settings import BACKEND_PORT

if __name__ == "__main__":
    start(app, BACKEND_PORT)