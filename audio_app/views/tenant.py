#
#!/usr/bin/python3.8 
#
# File: token.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: api route for setting tenant to microsoft
# for the stryker's audio data capturing tool application. 
#
from flask import Blueprint, request, make_response, jsonify, current_app
from ..services.ms_auth import set_ms_auth
from ..services.middleware import auth
import logging
from flask_cors import cross_origin
from ..services.schema import MStokenSchema
from ..services.helper import log_execution_time

tenant_bp = Blueprint('tenant', __name__)

@tenant_bp.route('/<session_id>/tenant', methods=['POST'])
@cross_origin()
@log_execution_time
def set_tenant_id(session_id):
    """
    set_tenant_id function used for setting the tenant id to user
    """      
    try:
        #validate request schema
        errors = MStokenSchema().validate(request.json)

        if errors:
            response = make_response(
                jsonify(
                    errors
                ),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            current_app.logger.error("An exception in MS token schema:",errors)
            return response


        req_data = request.get_json()
        current_app.logger.info("Set MS token")
        token_val = set_ms_auth(session_id, req_data)
        return token_val
    except Exception as error:
        current_app.logger.error("An exception occurred:", error)