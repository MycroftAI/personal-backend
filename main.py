from src.base import  app, start
from src.device import location, setting, get_uuid, code, device, activate,\
    send_mail, metric, subscription_type, get_subscriber_voice_url
from src.auth import pair, token
from src.stt import stt

if __name__ == "__main__":
    port = 6712
    start(app, port)