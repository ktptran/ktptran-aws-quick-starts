import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    request_id = event['pathParameters']['id']
    if not request_id:
        error = create_error("validation_error", "missing_id", "The id is an empty string")
        return create_response(400, {"error": error})

    try:
        result = delete_item_from_table(request_id)
        return create_response(200, {"todo": result})
    except Exception as e:
        print(str(e))
        return create_response(500)


def delete_item_from_table(request_id):
    """Deletes item from the todos table."""
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    response = table.delete_item(
        Key={
            'id': request_id
        }
    )
    return response


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
