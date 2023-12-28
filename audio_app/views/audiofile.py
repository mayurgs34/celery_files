#
#!/usr/bin/python3.8 
#
# File: audiofile.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: api route for audio file which download audio file and push to s3 
# for the stryker's audio data capturing tool application. 
#
from flask import Blueprint, jsonify, request, make_response, current_app
from ..services.helper import create_folder_s3, get_presigned_url_audiofile
from ..services.middleware import auth
from ..services.get_phrases import get_phrases
import requests
import os
import shutil
import logging
from flask_cors import cross_origin
from ..services.helper import log_execution_time
from .tasks import task_audio_file
import json

audiofile_bp = Blueprint('audiofile', __name__)

@audiofile_bp.route('/<campaign_name>/<session_id>/audiofile', methods=['POST','OPTIONS'])
# @cross_origin()
@log_execution_time
# @auth
def create_audio_file(campaign_name, session_id):
    """
    Create audio file the function used for uploading received audio file
    to s3 bucket based on campaign and session id using presigned url
    """      
    try:
        # get random phrases
        current_app.logger.info("Get random phrases")
        phrases_val = get_phrases(campaign_name)        

        args = request.args

        # check query param phrase_str is present
        if args.get("phrase_str") == None:
            response = make_response(
                jsonify(
                    {"message":'provide phrase_str in url'}
                ),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            current_app.logger.error('Provide phrase_str in url')
            return response

        # defining a name that will act as directory
        abspath = f'./audio_files/{campaign_name}' 
        try:
            os.makedirs(os.path.join(abspath, session_id), exist_ok=True)
        except OSError:
            current_app.logger.error("Creation of the directory %s failed" % abspath)
        else:
            current_app.logger.info("Successfully created the directory %s" % abspath)

        # check content type of received file
        if (len(request.files) == 0) or (request.files['audio_data'].content_type == None):
            response = make_response(
                jsonify(
                    {"error":'audio file not uploaded'}
                ),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            current_app.logger.error('Audio file not uploaded')
            return response

        if request.files['audio_data'].content_type not in ["audio/mpeg"]:
            response = make_response(
                jsonify(
                    {"message":'audio type not acceptable'}
                ),
                422,
            )
            response.headers["Content-Type"] = "application/json"
            current_app.logger.error('Audio type not acceptable')
            return response          

        PHRASE_WAV_PATH = f'./audio_files/{campaign_name}/{session_id}/{args.get("phrase_str")}.wav'

        if len(request.files) != 0:
            #save received to local environment
            audio_file_val = request.files['audio_data']
            audio_file_val.save(PHRASE_WAV_PATH)
            audio_file_val.flush()
            audio_file_val.close()

            #check audio file length, should not exceed 1MB
            file_size = os.path.getsize(PHRASE_WAV_PATH) 
            mb = file_size / 1024 / 1024
            if 1.0 < mb:
                os.remove(PHRASE_WAV_PATH)
                response = make_response(
                    jsonify(
                        {"message":'audio file size is greater than 1 MB'}
                    ),
                    400,
                )
                response.headers["Content-Type"] = "application/json"
                current_app.logger.error('Audio file size is greater than 1 MB')
                return response


        task_audio_file.delay(campaign_name, session_id, args.get("phrase_str"))

        response = make_response(
            jsonify(
                {"message":'audio file uploaded'}
            ),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        current_app.logger.info('Audio file uploaded')
        return response

        #create folder in s3 bucket
        create_folder_s3_resp = create_folder_s3(campaign_name, session_id)

        if not create_folder_s3_resp:
            response = make_response(
                jsonify(
                    {"message":"S3 folder not created"}
                ),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            current_app.logger.error("S3 folder not created")
            return response

        COUNTER = 3
        while COUNTER:
            response_val = get_presigned_url_audiofile(campaign_name, session_id, args.get("phrase_str"))

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
                response = make_response(
                    jsonify(
                        {"message":'audio file uploaded successfully'}
                    ),
                    200,
                )
                response.headers["Content-Type"] = "application/json"
                current_app.logger.info('Audio file uploaded successfully')
                return response
            
            COUNTER = COUNTER - 1

    except Exception as error:
        current_app.logger.error("An exception occurred:", error)    