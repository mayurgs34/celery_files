#
#!/usr/bin/python3.8 
#
# File: audiofile.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: api route for audio file which download audio file and push to s3 
# for the stryker's audio data capturing tool application. 
#
from flask import current_app
from ..services.helper import create_folder_s3, get_presigned_url_audiofile
import requests
import os
import shutil
from ..services.helper import log_execution_time
from celery import shared_task

@shared_task(bind=True)
def task_audio_file(self, campaign_name, session_id, phrase_str):
    """
    Create audio file the function used for uploading received audio file
    to s3 bucket based on campaign and session id using presigned url
    """      
    try:
        PHRASE_WAV_PATH = f'./audio_files/{campaign_name}/{session_id}/{phrase_str}.wav'


        #create folder in s3 bucket
        create_folder_s3_resp = create_folder_s3(campaign_name, session_id)

        if not create_folder_s3_resp:
            current_app.logger.error("S3 folder not created")
            return "False"

        COUNTER = 3
        while COUNTER:
            response_val = get_presigned_url_audiofile(campaign_name, session_id, phrase_str)

            #upload file to S3 using presigned URL
            file_path = PHRASE_WAV_PATH
            files = { 'file' : open(file_path, 'rb')}
            req = requests.post(response_val['url'], data=response_val['fields'], files=files)

            #prper file opening and closing openfile, test with unique request simultaneously
            
            if req.status_code == 204:
                try:
                    #after passing audio file to s3 , delele local content of session
                    folder_path = f'./audio_files/{campaign_name}/{session_id}'
                    shutil.rmtree(folder_path)
                    current_app.logger.info(f'{session_id} folder and its content removed')
                except:
                    current_app.logger.error(f'{session_id} folder not deleted')            
                current_app.logger.info('Audio file uploaded successfully')
                return "True"
            
            COUNTER = COUNTER - 1

            if self.is_aborted():
                return "TASK STOPPED"

    except Exception as error:
        current_app.logger.error("An exception occurred:", error)    