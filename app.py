#
#!/usr/bin/python3.8 
#
# File: app.py
# Author: Mayur Chavan (GSLab Pvt. Ltd. Pune)
# Date: 2023-11-23 18:49:59
# Functionality: Entry point for Backend flask code
# for the stryker's audio data capturing tool application. 
#
from audio_app import create_app

app, celery = create_app()
app.app_context().push()

if __name__ == '__main__':
    app.run()
















#req id and llogger
