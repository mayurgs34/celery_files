#
#!/usr/bin/python3.8 
#
# File: get_phrases.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: get the 50 random phrases for the stryker's audio data capturing tool application. 
#
import csv  
import pandas as pd
from flask import make_response, jsonify, current_app
import logging
from dotenv import load_dotenv, dotenv_values
import os
from ..services.helper import log_execution_time

#get 50 phrases from 50K phrases
@log_execution_time
def get_phrases(campaign_name):
    """
    Give the list of 50 randomly selected phrases from csv
    file based on passed campaign.

    Returns List of randomly selected 50 Phrases from csv
    """    
    load_dotenv()
    
    try:  
        CSV_PHRASE_PATH = os.getenv("CSV_PHRASE_PATH") + f'/{campaign_name}_phrases.csv'
        selected_phrases = None

        while True:
            df = pd.read_csv(CSV_PHRASE_PATH)
            df = df.sample(n=50)
            selected_phrases = [i[0] for i in df.values.tolist()]

            #remove duplicate and check count
            selected_phrases = list(set(selected_phrases))

            if len(selected_phrases) == 50:
                break

        response = make_response(
            jsonify(
                { "phrases" : selected_phrases} 
            ),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        current_app.logger.info("Read phrases from csv file")
        return response    
    except Exception as error:
        current_app.logger.error("An exception occurred:", error)
    response = make_response(
        jsonify(
            {"error":"Phrases not found for this region"} 
        ),
        404,
    )
    response.headers["Content-Type"] = "application/json"
    current_app.logger.error("Phrases not found for this region")
    return response