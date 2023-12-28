#
#!/usr/bin/python3.8 
#
# File: get_token.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: get the jwt token for the stryker's audio data capturing tool application. 
#
import jwt 
from datetime import datetime, timedelta
from functools import wraps
from flask import make_response, jsonify, current_app
from dotenv import load_dotenv, dotenv_values
import os
import logging
from ..services.helper import log_execution_time


@log_execution_time
def get_jwt_token(session_id):
    load_dotenv()
    """
    Give JWT token
    """    
    try:
        header = {  
          "alg": "HS256",  
          "typ": "JWT"  
        }     
 
        exp_time = datetime.now() + timedelta(minutes=21)
        exp_epoch_time = int(exp_time.timestamp())

        payload = {  
          "session_id": session_id,  
          "exp" : exp_epoch_time
        } 

        encoded_jwt = jwt.encode(payload, os.environ['SECRET_KEY'], algorithm='HS256', headers=header)  

        response = make_response(
            jsonify(
                { "token" : encoded_jwt} 
            ),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        current_app.logger.info("Create token")
        return response    
    except Exception as error:
        current_app.logger.error("An exception occurred:", error)