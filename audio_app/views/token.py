#
#!/usr/bin/python3.8 
#
# File: token.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: api route for getting jwt token
# for the stryker's audio data capturing tool application. 
#
from flask import Blueprint, current_app
from ..services.get_token import get_jwt_token
from ..services.middleware import auth
import logging
from flask_cors import cross_origin
from ..services.helper import log_execution_time

token_bp = Blueprint('token', __name__)

@token_bp.route('/<session_id>/auth', methods=['GET'])
@cross_origin()
@log_execution_time
def get_auth_token(session_id):
    """
    get_auth_token function used for getting the jwt token
    to validate the api request.
    """      
    try:

        current_app.logger.info("Get token")
        token_val = get_jwt_token(session_id)
        return token_val
    except Exception as error:
        current_app.logger.error("An exception occurred:", error)