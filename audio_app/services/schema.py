#
#!/usr/bin/python3.8 
#
# File: schema.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: list of field which are mandatory in json body of metadata api 
# for the stryker's audio data capturing tool application. 
#
from marshmallow import Schema, fields

"""
Schema for metadata json, to get the details of 
Browser. these are the mandatory fields.
"""
class MetadataRequestSchema(Schema):
    accent = fields.Str(required=True)
    browser = fields.Str(required=True)
    browser_version = fields.Str(required=True)
    device = fields.Str(required=True) 
    timestamp = fields.Str(required=True) 
    session_id = fields.Str(required=True)    
    campaign_name = fields.Str(required=True) 
    ms_token_id = fields.Str(required=True) 
    ms_token_title = fields.Str(required=True) 
    language = fields.Str(required=True)
    user_agent = fields.Str(required=True)

class MStokenSchema(Schema):
    name_text = fields.Str(required=True)
    email_text = fields.Str(required=True)