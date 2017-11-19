# Serverless REST API implementation of a Key/Value Service

Implementation of a basic key/value service. Uses a RESTful API with AWS Lambda.
DynamoDB is used to store the data.

## Setup

### Prerequisites

1. `python`
2. `virtualenv`
3. `node`

### Installing

After cloning, make sure you have serverless installed:

```
npm install -g serverless
```

Follow these instructions to setup AWS credentials:

https://serverless.com/framework/docs/providers/aws/guide/credentials/


Create a new virtualenv, then:

```bash
npm install
pip install -r requirements.txt
```

## Deploy

In order to deploy the endpoint simply run

```bash
serverless deploy
```

The expected result should be similar to:

```bash
Serverless: Installing required Python packages with python2.7...
Serverless: Linking required Python packages...
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Unlinking required Python packages...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service .zip file to S3 (1.92 MB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
......................................
Serverless: Stack update finished...
Service Information
service: kv-lambda
stage: dev
region: us-west-2
stack: kv-lambda-dev
api keys:
  None
endpoints:
  GET - https://fj24zx740e.execute-api.us-west-2.amazonaws.com/dev/v1/key
  GET - https://fj24zx740e.execute-api.us-west-2.amazonaws.com/dev/v1/key/{key}
  POST - https://fj24zx740e.execute-api.us-west-2.amazonaws.com/dev/v1/key
  PUT - https://fj24zx740e.execute-api.us-west-2.amazonaws.com/dev/v1/key/{key}
  DELETE - https://fj24zx740e.execute-api.us-west-2.amazonaws.com/dev/v1/key/{key}
functions:
  list: kv-lambda-dev-list
  get: kv-lambda-dev-get
  create: kv-lambda-dev-create
  update: kv-lambda-dev-update
  delete: kv-lambda-dev-delete
```

## Usage

You can create, retrieve, update, or delete keys with the following commands:

### Create a Key

```bash
curl -X POST https://fj24zx740e.execute-api.us-west-2.amazonaws.com/dev/v1/key --data '{ "key": "sports", "value":"baseball" }'
```

### List all Keys

```bash
curl https://fj24zx740e.execute-api.us-west-2.amazonaws.com/dev/v1/key
```

### Get one Key

```bash
# Replace the <key> part with a real key from your keys table
curl https://fj24zx740e.execute-api.us-west-2.amazonaws.com/dev/v1/key/<key>
```

### Update a Key

```bash
# Replace the <key> part with a real key from your keys table
curl -X PUT https://fj24zx740e.execute-api.us-west-2.amazonaws.com/dev/v1/key/<key> --data '{"value": "football"}'
```

### Delete a Key

```bash
# Replace the <key> part with a real key from your keys table
curl -X DELETE https://fj24zx740e.execute-api.us-west-2.amazonaws.com/dev/v1/key/<key>
```

## Testing

Tests are written with `pytest` and `moto`

Run them with `python tests.py`

### Further Testing

AWS Lambda allows configuration of test events in its Lambda service.

Also, a Test Harness blueprint exists for AWS Lambda, but it currently only supports Node runtimes.
This blueprint can probably be ported over to Python, which could be a fun but separate project.
More info here: https://aws.amazon.com/blogs/compute/serverless-testing-with-aws-lambda/
