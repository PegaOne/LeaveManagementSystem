# import the json utility package since we will be working with a JSON object
import json
# import the AWS SDK (for Python the package name is boto3)
import boto3

from boto3.dynamodb.conditions import Key

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table('LeaveDB')

# define the handler function that the Lambda service will use as an entry point
def lambda_handler(event, context):
    emailID = event['emailID']
    response = table.query(
    KeyConditionExpression=Key('emailID').eq(emailID)
    )
    return response
