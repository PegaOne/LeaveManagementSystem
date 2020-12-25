import json

CLIENT_ID = 'blah-blah-long-string'
CLIENT_SECRET = 'blah-blah-really-long-string'

def lambda_handler(event, context):
    event['response'] = {
        "autoConfirmUser" : True
    }
    return event
