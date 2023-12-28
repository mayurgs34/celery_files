#
#!/usr/bin/python3.8 
#
# File: get_token.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: set the MS token for the stryker's audio data capturing tool application. 
#
from datetime import datetime, timedelta
from functools import wraps
from flask import make_response, jsonify, current_app
from dotenv import load_dotenv, dotenv_values
import os
import logging 
import requests
from requests.exceptions import HTTPError
import time
from .token_data import get_token_data, set_token_data
import string
import random
from datetime import datetime
import json
from ..services.helper import log_execution_time

@log_execution_time
def set_ms_auth(session_id, req_data):
    load_dotenv()
    """
    Set MS token
    """    
    try:
        response = None
        counter = 0
        id_val = None
        title_val = None

        while True:        
            # 1. get token
            token_val = get_token_data()
            if token_val == None:
                raise Exception("Error in token generation")

            # 2. hit api 
            # POST data to MS login
            endpoint = f"https://graph.microsoft.com/v1.0/sites/{os.environ['site_id']}/lists/{os.environ['list_id']}/items"

            data_body = {
                            "fields": {
                                "Datesentout": datetime.now().strftime("%Y%m%d"),
                                "Datecompleted": datetime.now().strftime("%Y%m%d"),
                                "Requester": "Audio Collection Tool",
                                "Title": ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
                                "Consenteename": req_data['name_text'],
                                "Template": "SACT_01",
                                "Emailaddress": req_data['email_text'],
                                "Status": "Completed",
                                "ContentType": "Item"
                            }
                        }

            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token_val}'}
            response = requests.post(endpoint, data=json.dumps(data_body, indent = 4) , headers=headers)

            # 3. if 201 then break            
            if response.status_code == 201:
                id_val = response.json()['fields']['id']
                title_val = response.json()['fields']['Title']
                break

            # 4. if not 201 then set token 
            if response.status_code == 401:
                response = None
                set_token_data()
            
            counter = counter + 1
            if counter > 3: 
                break

        # If the response was successful, no Exception will be raised
        if response == None:
            response.raise_for_status()
    except HTTPError as http_err:
        current_app.logger.error(f'HTTP error occurred: {http_err}')  
        response = make_response(
            jsonify(
                {"message":f"Error when generating the token http_err {http_err}"} 
            ),
            400,
        )
        response.headers["Content-Type"] = "application/json"
        current_app.logger.error("Error when generating the token http_err")
        return response        
    except Exception as err:
        current_app.logger.error(f'Error occurred: {err}')  

        response = make_response(
            jsonify(
                {"message":f"Error when generating the token err {err}"} 
            ),
            400,
        )
        response.headers["Content-Type"] = "application/json"
        current_app.logger.error("Error when generating the token err")
        return response

    else:
        current_app.logger.info('Success!')  
        response = make_response(
            jsonify(
                { 
                    "Message" : "Token generated successfully",
                    "id_val" : id_val,
                    "title_val" : title_val
                 } 
            ),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        current_app.logger.info("Create MS token")
        return response        