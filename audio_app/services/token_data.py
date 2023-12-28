from dotenv import load_dotenv, dotenv_values
import requests
import logging
from requests.exceptions import HTTPError
import os
from flask import current_app
from ..services.helper import log_execution_time

token_data=""

# Refresh token if token time expired
@log_execution_time
def set_token_data(): 
    load_dotenv()
    """
    Set MS token
    """
    response = None
    counter = 0
    try:
        while True:
            # 1. get token hit api 
            endpoint = f"https://login.microsoftonline.com/{os.environ['tenant_id']}/oauth2/v2.0/token"

            data_body = {
                "grant_type" : "client_credentials",
                "scope" : "https://graph.microsoft.com/.default",
                "client_id" : os.environ['client_id'], 
                "client_secret" : os.environ['client_secret'] 
            }

            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

            # 2. api response
            response = requests.post(endpoint, data=data_body, headers=headers)

            access_token = response.json()

            global token_data 
            token_data = access_token['access_token']
            
            counter = counter + 1
            # 3. if 200 then return            
            if response.status_code() == 200:
                return token_data
            
            response = None
            if counter > 3: 
                break

        # 4. If the response was successful, no Exception will be raised
        if response == None:
            response.raise_for_status()
    except HTTPError as http_err:
        current_app.logger.error(f'HTTP error occurred: {http_err}')         
    except Exception as err:
        current_app.logger.error(f'Error occurred: {err}')  
    return response


@log_execution_time
def get_token_data(): 
    """
    get MS token
    """
    global token_data 
    return token_data