#
#!/usr/bin/python3.8 
#
# File: phrases.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: api route for getting the list f 50 random phrases from config
# Folder as per the campaign 
# for the stryker's audio data capturing tool application. 
#
from flask import Blueprint, request, current_app
from ..services.get_phrases import get_phrases
from ..services.middleware import auth
import logging
from flask import make_response, jsonify
from flask_cors import cross_origin
from ..services.helper import log_execution_time

phrases_bp = Blueprint('phrases', __name__)

#returning 50 phrases 
@phrases_bp.route('/<campaign_name>/phrases', methods=['GET','OPTIONS'])
@cross_origin()
@log_execution_time
@auth
def get_phrases_data(campaign_name):
    """
    get_phrases_data function used for getting the 50 random 
    phrases from csv file object based on campaign.
    """      
    try:        
        # get random phrases for campaign
        current_app.logger.info(f"Get random phrases for campaign {campaign_name}")#CHECK RETURN VALUE
        phrases_val = get_phrases(campaign_name)
        return phrases_val
    except Exception as error:
        current_app.logger.error("An exception occurred:", error)