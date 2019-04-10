from flask import request
import time
import json
from os.path import join
from personal_mycroft_backend.backend.decorators import noindex
from personal_mycroft_backend.settings import PRECISE_DATA_FOLDER


def get_precise_routes(app):
    @app.route('/precise/upload', methods=['POST'])
    @noindex
    def precise_upload():
        uploads = request.files
        for precisefile in uploads:
            fn = uploads[precisefile].filename
            if fn == 'audio':
                name = (str(int(time.time()))) + ".wav"
                uploads[precisefile].save(os.path.join(app.config['PRECISE_DATA_FOLDER'], name))
            
            if fn == 'metadata':
                name =  (str(int(time.time()))) + ".meta"
                uploads[precisefile].save(os.path.join(app.config['PRECISE_DATA_FOLDER'], name))

    return app
