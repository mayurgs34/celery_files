#
#!/usr/bin/python3.8 
#
# File: app.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: List of routes of api
# for the stryker's audio data capturing tool application. 
#
from flask import Flask
from flask_marshmallow import Marshmallow
import logging
from flask_cors import CORS

from logging.config import dictConfig
from .views.utils import make_celery

def create_app():
    API_PATH = "/api/v1/campaign"
    app = Flask(__name__)

    with app.app_context():
        cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
        ma = Marshmallow(app)
        dictConfig({
            'version': 1,
            'formatters': {'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s.py : %(message)s',
            }},
            'handlers': {'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }},
            'root': {
                'level': 'INFO',
                'handlers': ['wsgi']
            }
        })

        app.config['CELERY_RESULT_BACKEND'] = "rpc://"
        app.config['CELERY_BROKER_URL'] = "amqp://guest:guest@rabbit:5672"

        celery = make_celery(app)
        celery.set_default()

    from .views.metadata import metadata_bp
    from .views.audiofile import audiofile_bp
    from .views.phrases import phrases_bp
    from .views.token import token_bp
    from .views.tenant import tenant_bp


    app.register_blueprint(phrases_bp, url_prefix=API_PATH)
    app.register_blueprint(metadata_bp, url_prefix=API_PATH)
    app.register_blueprint(audiofile_bp, url_prefix=API_PATH)
    app.register_blueprint(token_bp, url_prefix=API_PATH)
    app.register_blueprint(tenant_bp, url_prefix=API_PATH)

    return app, celery
