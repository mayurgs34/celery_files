#
#!/usr/bin/python3.8 
#
# File: metadata.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: api route for metadata to push to s3 
# for the stryker's audio data capturing tool application. 
#
from flask import Blueprint, jsonify, request, make_response, current_app
from ..services.helper import create_folder_s3, get_presigned_url_metadata
from ..services.middleware import auth
from ..services.get_phrases import get_phrases
import requests
import json
from ..services.schema import MetadataRequestSchema
import logging
from flask_cors import cross_origin
from ..services.helper import log_execution_time

metadata_bp = Blueprint('metadata', __name__)

# #upload meta data to s3 bucket
@metadata_bp.route('/<campaign_name>/<session_id>/metadata', methods=['POST','OPTIONS'])
@cross_origin()
@log_execution_time
@auth
def post_meta_data(campaign_name, session_id):
    """
    post_meta_data the function used for creating meta data on s3 
    using campaign and session id.
    """     
    #check camp, 404 not found 
    try:
        current_app.logger.info("Latest changes added")
        # get random phrases
        current_app.logger.info("Get random phrases")
        phrases_val = get_phrases(campaign_name)

        #validate request schema
        errors = MetadataRequestSchema().validate(request.json)

        if errors:
            response = make_response(
                jsonify(
                    errors
                ),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            current_app.logger.error("An exception in metadata schema:",errors)
            return response

        #create folder
        create_folder_s3_resp = create_folder_s3(campaign_name, session_id)

        if not create_folder_s3_resp:
            response = make_response(
                jsonify(
                    {"message":"S3 folder not properly created"}
                ),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            current_app.logger.error("S3 folder not properly created")
            return response


        #generate presigned_url
        response_val = get_presigned_url_metadata(campaign_name,session_id)

        # Convert Dictionary to JSON String
        data_string = json.dumps(json.loads(request.data), indent=2, default=str)
        files = { 'file' : data_string}

        #upload file to S3 using presigned URL
        req = requests.post(response_val['url'], data=response_val['fields'], files=files)
        
        if req.status_code == 204:
            response = make_response(
                jsonify(
                    {"message":"metadata uploaded successfully w=2 t=2"}
                ),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            current_app.logger.info("Metadata uploaded successfully")
            return response

        response = make_response(
            jsonify(
                {"error":"metadata not properly uploaded"}
            ),
            422,
        )
        response.headers["Content-Type"] = "application/json"
        current_app.logger.error("Metadata not properly uploaded")
        return response    
    except Exception as error:  
        current_app.logger.error("An exception occurred:", error)