################################
# Slack Lambda handler.
################################

import boto3
import logging
import os
import urllib

# Grab data from the environment.
BOT_TOKEN   = os.environ["BOT_TOKEN"]
ASSET_TABLE = os.environ["ASSET_TABLE"]
REGION_NAME = os.getenv('REGION_NAME', 'us-east-1')

dynamo = boto3.resource('dynamodb', region_name=REGION_NAME, endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

# Define the URL of the targeted Slack API resource.
SLACK_URL = "https://slack.com/api/chat.postMessage"

def getAssetExistance(asset):
    dynamoTable = dynamo.Table('Assets')
    response    = dynamoTable.query(KeyConditionExpression=Key('userID').eq(asset))

    return bool(response)

def lambda_handler(data, context):
    # Slack challenge answer.
    if "challenge" in data:
        return data["challenge"]

    # Grab the Slack channel data.
    slack_event    = data['event']
    slack_userID   = slack_event["user"]
    slack_text     = slack_event["text"]
    channel_id     = slack_event["channel"]
    slack_reply    = ""

    # Ignore bot messages.
    if "bot_id" in slack_event:
        slack_reply = ""
    else:

        # Start data sift.
        if slack_text.startswith("!networth"):
            slack_reply = "Your networth is: "
        elif slack_text.startswith("!price"):
            command,asset = text.split()
            slack_reply = "The price of a(n) %s is: " % (asset)
        elif slack_text.startswith("!addme"):
            if not getAssetExistance(slack_userID):
                slack_reply = "Adding user: %s" % (slack_userID)
                dynamo.update_item(TableName=ASSET_TABLE,
                    Key={'userID':{'S':'slack_userID'}},
                    AttributeUpdates= {
                        'resources':{
                            'Action': 'ADD',
                            'Value': {'N': '1000'}
                        }
                    }
                )
            else:
                slack_reply = "User %s already exists" % (slack_userID)

        # We need to send back three pieces of information:
        data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", channel_id),
                ("text", slack_reply)
            )
        )
        data = data.encode("ascii")

        # Construct the HTTP request that will be sent to the Slack API.
        request = urllib.request.Request(
            SLACK_URL,
            data=data,
            method="POST"
        )
        # Add a header mentioning that the text is URL-encoded.
        request.add_header(
            "Content-Type",
            "application/x-www-form-urlencoded"
        )

        # Fire off the request!
        urllib.request.urlopen(request).read()

    # Everything went fine.
    return "200 OK"
