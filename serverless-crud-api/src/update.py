import json
import time
import os

from src import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    request_id = event['pathParameters']['id']
    if not request_id:
        error = create_error("validation_error", "missing_id", "The id is an empty string")
        return create_response(400, {"error": error})

    request, error = validate_request(event['body'])
    if (error != None):
        return create_response(400, {"error": error})

    try:
        attributes = update_item_in_table(request, request_id)
        return create_response(200, attributes)
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
    elif 'checked' not in request:
        code, message = 'missing_checked', 'Checked is missing'

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
        response['body'] = json.dumps(body,
                           cls=decimalencoder.DecimalEncoder)

    return response


def update_item_in_table(request, request_id):
    """Updates the item in the table and returns."""
    timestamp = int(time.time() * 1000)
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.update_item(
        Key={
            'id': request_id
        },
        ExpressionAttributeNames={
            '#todo_task': 'task'
        },
        ExpressionAttributeValues={
            ':task': request['task'],
            ':checked': request['checked'],
            ':updatedAt': timestamp,
        },
        UpdateExpression='SET #todo_task = :task, '
                         'checked = :checked, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW'
    )
    return result['Attributes']
