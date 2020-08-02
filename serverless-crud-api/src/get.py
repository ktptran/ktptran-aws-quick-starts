import os
import json

from src import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    request_id = event['pathParameters']['id']

    if not request_id:
        error = create_error("validation_error", "missing_id", "The id is an empty string")
        return create_response(400, {"error": error})

    try:
        item = get_item_from_table(request_id)
        if item == None:
            error = create_error('not_found_error', 'not_found', 'Todo with id does not exist.')
            return create_response(400, {"error": error})
        return create_response(200, {"todo": item})
    except Exception as e:
        print(str(e))
        return create_response(500)


def get_item_from_table(request_id):
    """Retrieve item from the todos table."""
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.get_item(
        Key={
            'id': request_id
        }
    )
    if 'Item' not in result:
        return None
    return result['Item']


def create_error(error_type, code, message):
    """Generates error that gets returned"""
    return {
        'type': error_type,
        'code': code,
        'message': message
    }


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
