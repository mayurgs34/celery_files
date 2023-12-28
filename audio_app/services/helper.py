#
#!/usr/bin/python3.8 
#
# File: helper.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: methods to get presigned  url which used to pass data to s3 bucket
# the stryker's audio data capturing tool application. 
#
import boto3
from dotenv import load_dotenv, dotenv_values
import os
from flask import make_response, jsonify, current_app
import logging
from datetime import date
import time
from functools import wraps

def log_execution_time(func):
    """This decorator prints the execution time for the decorated function."""
    @wraps(func)
    def execution_tim_logger(*args, **kwargs):
        start = time.time()
        current_app.logger.info('Starting execution of - {}'.format(func.__name__))
        result = func(*args, **kwargs)
        end = time.time()
        current_app.logger.info("{} was executed in {}s".format(func.__name__, round(end - start, 2)))
        return result
    return execution_tim_logger

#create folder path for campaign in s3 bucket
@log_execution_time
def get_s3_path(campaign_name,session_id):
    #get todays date and create path string
    today = date.today()
    path_str = f'campaigns/{campaign_name}_Campaign/{today.strftime("%Y/%m/%d")}/{session_id}/'
    return path_str

# #create subfolder in campaign
# @log_execution_time
# def create_folder_s3(campaign_name:str,session_id: str):
#     """
#     Create folder based on campaign and session id in s3 
#     bucket and use it to add json and audio file. 
#     """      
#     load_dotenv()

#     #get object of s3 bucket
#     s3 = boto3.client('s3', region_name=os.environ['AWS_REGION'])

#     #create path for s3 object
#     subfolder = get_s3_path(campaign_name,session_id)
    
#     try:
#         #create object in target bucket
#         s3.put_object(Bucket=os.environ['TARGET_BUCKET'], Key=subfolder)

#         current_app.logger.info("Create object in target bucket")
#         return True
#     except Exception as error:
#         current_app.logger.error("An exception occurred:", error)

#     return False

# #get presigned url for meta data
# @log_execution_time
# def get_presigned_url_metadata(campaign_name:str,session_id: str):
#     try:    
#         """
#         Create and get presigned url for s3 metadata based on
#         campaign name and session id.

#         Returns dict containing link for presigned url
#         """    
#         load_dotenv()

#         #get object of s3 bucket
#         s3 = boto3.client('s3', region_name=os.environ['AWS_REGION'])

#         #create path for s3 object
#         subfolder = get_s3_path(campaign_name,session_id)
#         meta_data_file = "meta-info.json"
        
#         #get presigned url based on path given
#         response = s3.generate_presigned_post(Bucket=os.environ['TARGET_BUCKET'], Key=subfolder + meta_data_file, ExpiresIn=10)
#         current_app.logger.info("Get presigned url for metadata based on path given")

#         return response
#     except Exception as error: 
#         current_app.logger.error("An exception occurred:Lastest", error)

# #get presigned url for audio file
# @log_execution_time
# def get_presigned_url_audiofile(campaign_name:str,session_id: str, phrase_str: str):
#     try:
#         """
#         Create and get presigned url for s3 audiofile based on
#         campaign name and session id

#         Returns dict containing link for presigned url
#         """       
#         load_dotenv()

#         #get object of s3 bucket
#         s3 = boto3.client('s3', region_name=os.environ['AWS_REGION'])

#         #create path for s3 object
#         subfolder = get_s3_path(campaign_name,session_id)
#         audiofile = phrase_str + ".wav"
        
#         #get presigned url based on path given
#         response = s3.generate_presigned_post(Bucket=os.environ['TARGET_BUCKET'], Key=subfolder + audiofile, ExpiresIn=10)
#         current_app.logger.info("Get presigned url for audiofile based on path given")

#         return response
#     except Exception as error:
#         current_app.logger.error("An exception occurred:", error)

#

#!/usr/bin/python3.8 

#

# File: helper.py

# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)

# Date: 2023-11-23 18:49:59

# Functionality: methods to get presigned  url which used to pass data to s3 bucket

# the stryker's audio data capturing tool application. 

#



#create folder path for campaign in s3 bucket
@log_execution_time
def get_s3_path(campaign_name,session_id):

    #get todays date and create path string

    today = date.today()

    path_str = f'campaigns/{campaign_name}_Campaign/{today.strftime("%Y/%m/%d")}/{session_id}/'

    return path_str

#create subfolder in campaign
@log_execution_time
def create_folder_s3(campaign_name:str,session_id: str):

    """

    Create folder based on campaign and session id in s3 

    bucket and use it to add json and audio file. 

    """      

    load_dotenv()

    #get object of s3 bucket

    s3 = boto3.client('s3',aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 

                  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), 

                  aws_session_token=os.getenv("AWS_SESSION_TOKEN"))

    #create path for s3 object

    subfolder = get_s3_path(campaign_name,session_id)

    

    try:

        #create object in target bucket

        s3.put_object(Bucket=os.getenv("TARGET_BUCKET"), Key=subfolder)

        logging.info("create object in target bucket")

        return True

    except Exception as error:

        logging.error("An exception occurred:", error)

    return False

#get presigned url for meta data
@log_execution_time
def get_presigned_url_metadata(campaign_name:str,session_id: str):

    try:    

        """

        Create and get presigned url for s3 metadata based on

        campaign name and session id.

        Returns dict containing link for presigned url

        """    

        load_dotenv()

        #get object of s3 bucket

        s3 = boto3.client('s3',aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 

                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), 

                    aws_session_token=os.getenv("AWS_SESSION_TOKEN"))

        #create path for s3 object

        subfolder = get_s3_path(campaign_name,session_id)

        meta_data_file = "meta-info.json"

        

        #get presigned url based on path given

        response = s3.generate_presigned_post(Bucket=os.getenv("TARGET_BUCKET"), Key=subfolder + meta_data_file, ExpiresIn=10)

        logging.info("get presigned url for metadata based on path given")

        return response

    except Exception as error: 

        logging.error("An exception occurred:", error)

#get presigned url for audio file
@log_execution_time
def get_presigned_url_audiofile(campaign_name:str,session_id: str, phrase_str: str):

    try:

        """

        Create and get presigned url for s3 audiofile based on

        campaign name and session id

        Returns dict containing link for presigned url

        """       

        load_dotenv()

        #get object of s3 bucket

        s3 = boto3.client('s3',aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 

                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), 

                    aws_session_token=os.getenv("AWS_SESSION_TOKEN"))

        #create path for s3 object

        subfolder = get_s3_path(campaign_name,session_id)

        audiofile = phrase_str + ".wav"

        

        #get presigned url based on path given

        response = s3.generate_presigned_post(Bucket=os.getenv("TARGET_BUCKET"), Key=subfolder + audiofile, ExpiresIn=10)

        logging.info("get presigned url for audiofile based on path given")

        return response

    except Exception as error:

        logging.error("An exception occurred:", error)

