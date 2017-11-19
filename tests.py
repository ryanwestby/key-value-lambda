import pytest
from moto import mock_dynamodb2
import handler
import json


@pytest.yield_fixture(scope='function')
def dynamodb_fixture(monkeypatch):
    mock_dynamodb2().start()

    client = handler.get_dynamodb_conn()
    client.create_table(TableName='TestTable',
                        KeySchema=[{
                            'AttributeName': 'key',
                            'KeyType': 'HASH'
                        }],
                        AttributeDefinitions=[{
                            'AttributeName': 'key',
                            'AttributeType': 'S'
                        }],
                        ProvisionedThroughput={
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        })
    monkeypatch.setenv('DYNAMODB_TABLE', 'TestTable')

    yield client

    mock_dynamodb2().stop()


@pytest.yield_fixture(scope='function')
def put_item(dynamodb_fixture):
    table = dynamodb_fixture.Table('TestTable')
    item = {
        'key': 'sports',
        'value': 'baseball'
    }
    table.put_item(Item=item)

    yield item

    table.delete_item(Key={
        'key': 'sports'
    })


def test_list(put_item):
    list_resp = handler.list(None, None)
    assert json.loads(list_resp['body']) == [put_item]

    # Delete item then test for empty list
    event = {
        'pathParameters': {
            'key': 'sports'
        }
    }
    handler.delete(event, None)
    list_resp2 = handler.list(None, None)
    assert json.loads(list_resp2['body']) == []


def test_get(put_item):
    # Get request looks like: https://XXXXXXXXXX.execute-api.us-west-2.amazonaws.com/dev/v1/key/{key}
    # Path parameters are sent to event object
    event = {
        'pathParameters': {
            'key': 'sports'
        }
    }
    get_resp = handler.get(event, None)
    assert json.loads(get_resp['body']) == put_item['value']


def test_get_404(put_item):
    event = {
        'pathParameters': {
            'key': 'games'
        }
    }
    get_resp = handler.get(event, None)
    assert get_resp['statusCode'] == 404


def test_create(dynamodb_fixture):
    body = {
            'key': 'sports',
            'value': 'baseball'
        }
    event = {
        'body': json.dumps(body)
    }
    create_resp = handler.create(event, None)
    assert create_resp['body'] == event['body']

    table = dynamodb_fixture.Table('TestTable')
    scan_resp = table.scan()
    assert scan_resp['Items'][0] == body

    # Test list returns item after item is created
    list_resp = handler.list(None, None)
    assert json.loads(list_resp['body'])[0] == body


def test_create_404(dynamodb_fixture):
    # Test missing key
    body = {
            'value': 'baseball'
        }
    event = {
        'body': json.dumps(body)
    }
    create_resp = handler.create(event, None)
    assert create_resp['statusCode'] == 404

    # Test missing value
    body = {
            'key': 'sports'
        }
    event = {
        'body': json.dumps(body)
    }
    create_resp = handler.create(event, None)
    assert create_resp['statusCode'] == 404


def test_update(put_item):
    body = {
            'value': 'football'
        }
    event = {
        'body': json.dumps(body),
        'pathParameters': {
            'key': 'sports'
        }
    }
    json_update_resp = handler.update(event, None)
    resp = json.loads(json_update_resp['body'])
    assert resp['key'] == put_item['key']
    assert resp['value'] == body['value']


def test_update_404(put_item):
    # Test key that doesn't exist
    body = {
            'value': 'football'
        }
    event = {
        'body': json.dumps(body),
        'pathParameters': {
            'key': 'games'
        }
    }
    update_resp = handler.update(event, None)
    assert update_resp['statusCode'] == 404

    # Test missing value
    body = {
        }
    event = {
        'body': json.dumps(body),
        'pathParameters': {
            'key': 'sports'
        }
    }
    update_resp = handler.update(event, None)
    assert update_resp['statusCode'] == 404


def test_delete(dynamodb_fixture, put_item):
    event = {
        'pathParameters': {
            'key': 'sports'
        }
    }
    delete_resp = handler.delete(event, None)
    assert delete_resp['statusCode'] == 200

    # Key should not exist
    get_resp = handler.get(event, None)
    assert get_resp['statusCode'] == 404
