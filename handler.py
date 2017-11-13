import os
import json

import boto3

DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
dynamodb = boto3.resource('dynamodb')


def list(event, context):
    table = dynamodb.Table(DYNAMODB_TABLE)

    result = table.scan()

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response


def get(event, context):
    table = dynamodb.Table(DYNAMODB_TABLE)

    result = table.get_item(
        Key={
            'key': event['pathParameters']['key']
        }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item']['value'])
    }

    return response


def create(event, context):
    table = dynamodb.Table(DYNAMODB_TABLE)
    data = json.loads(event['body'])

    if 'key' not in data:
        raise Exception("Couldn't create item, needs key.")
        return
    if 'value' not in data:
        raise Exception("Couldn't create item, needs value.")
        return

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
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    data = json.loads(event['body'])

    if 'value' not in data:
        raise Exception("Couldn't update the item.")
        return

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

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'])
    }

    return response


def delete(event, context):
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
