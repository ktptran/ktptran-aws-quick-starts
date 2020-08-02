import json
import os

from src import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    """Lists all tasks in the todo table."""
    try:
        items = list_items_from_table()
        return create_response(200, items)
    except Exception as e:
        print(str(e))
        return create_response(500)


def list_items_from_table():
    """Gets all the items from the table."""
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.scan()
    return result['Items']


def create_response(status_code, body=None):
    """Generates the response that gets returned"""
    response = {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }

    if (body != None):
        response['headers']['Content-Type'] = 'application/json'
        response['body'] = json.dumps(body,
                           cls=decimalencoder.DecimalEncoder)

    return response
