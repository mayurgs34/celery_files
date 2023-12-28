#
#!/usr/bin/python3.8 
#
# File: middleware.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: auth decorator is used to validate api 
# for the stryker's audio data capturing tool application. 
#
from dotenv import load_dotenv
from flask import request, make_response, jsonify, current_app
import logging
import functools
import os
import jwt

def auth(view_func):
    @functools.wraps(view_func)
    def decorated(*args, **kwargs):
        """
        Middleware for authenticating apis, Check if the api is having 
        valid signature
        """        
        load_dotenv()

        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            response = make_response(
                jsonify(
                    {
                        "message": "Authentication Token is missing!",
                        "data": None,
                        "error": "Unauthorized"
                    }
                ),
                401,
            )
            response.headers["Content-Type"] = "application/json"
            current_app.logger.error("Authentication Token is missing!")
            return response         
        try:
            data=jwt.decode(token, os.environ['SECRET_KEY'], algorithms=["HS256"])
            session_id=data["session_id"]
            if session_id is None:
                response = make_response(
                    jsonify(
                        {
                            "message": "Invalid Authentication token!",
                            "data": None,
                            "error": "Unauthorized"
                        }
                    ),
                    401,
                )
                response.headers["Content-Type"] = "application/json"
                current_app.logger.error("Invalid Authentication token!")
                return response 

        except Exception as e:
            response = make_response(
                jsonify(
                    {
                        "message": "Something went wrong",
                        "data": None,
                        "error": str(e)
                    }
                ),
                500,
            )
            response.headers["Content-Type"] = "application/json"
            current_app.logger.error("Something went wrong")
            return response 

        return view_func(*args, **kwargs)

    return decorated        