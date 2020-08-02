import json
import os
import uuid
import json
import time

import boto3
dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    request, error = validate_request(event['body'])
    if (error != None):
        return create_response(400, {"error": error})

    try:
        item = put_item_in_table(request['task'])
        return create_response(200, json.dumps(item))
    except Exception as e:
        print(str(e))
        return create_response(500)


def validate_request(body):
    """Validates the given request for the required parameters."""
    code, message = None, None

    try:
        request = json.loads(body)
    except json.JSONDecodeError:
        return None, create_error('validation_error,', 'json_parsing_error', 'JSON Parsing Exception')

    if 'task' not in request:
        code, message = 'missing_task', 'Task is missing'
    elif not request['task']:
        code, message = 'incomplete_task', 'Task is an empty string.'

    if (code != None or message != None):
        return None, create_error('validation_error', code, message)

    return request, None


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
        response['body'] = json.dumps(body)

    return response


def put_item_in_table(task):
    """Adds the request parameters into the table and returns."""
    timestamp = str(time.time())
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    item = {
        'id': str(uuid.uuid4()),
        'task': task,
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    table.put_item(Item=item)
    return item
