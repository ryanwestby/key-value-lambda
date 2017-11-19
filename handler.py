import os
import json

import boto3


def get_dynamodb_conn():
    return boto3.resource('dynamodb')


def list(event, context):
    dynamodb = get_dynamodb_conn()
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.scan()

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response


def get(event, context):
    dynamodb = get_dynamodb_conn()
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    result = table.get_item(
        Key={
            'key': event['pathParameters']['key']
        }
    )

    try:
        value = json.dumps(result['Item']['value'])
        response = {
            "statusCode": 200,
            "body": value
        }
    except KeyError:
        response = {
            "statusCode": 404,
            "body": "Item not found"
        }

    return response


def create(event, context):
    dynamodb = get_dynamodb_conn()
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    data = json.loads(event['body'])

    if 'key' not in data:
        response = {
            "statusCode": 404,
            "body": "Couldn't create item, needs key."
        }
        return response
    if 'value' not in data:
        response = {
            "statusCode": 404,
            "body": "Couldn't create item, needs value."
        }
        return response

    item = {
        'key': data['key'],
        'value': data['value']
    }

    table.put_item(Item=item)

    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response


def update(event, context):
    dynamodb = get_dynamodb_conn()
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    data = json.loads(event['body'])

    if 'value' not in data:
        response = {
            "statusCode": 404,
            "body": "Couldn't update item, needs value."
        }
        return response

    result = table.update_item(
        Key={
            'key': event['pathParameters']['key']
        },
        ExpressionAttributeNames={
            '#value': 'value',
        },
        ExpressionAttributeValues={
            ':value': data['value'],
        },
        UpdateExpression='SET #value = :value',
        ReturnValues='ALL_NEW',
    )

    if not result['Attributes']:
        response = {
            "statusCode": 404,
            "body": "Key not found"
        }
    else:
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Attributes'])
        }

    return response


def delete(event, context):
    dynamodb = get_dynamodb_conn()
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    table.delete_item(
        Key={
            'key': event['pathParameters']['key']
        }
    )

    response = {
        "statusCode": 200
    }

    return response
