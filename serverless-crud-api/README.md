<!--
title: 'AWS Serverless CRUD API with DynamoDB store quick start in Python'
description: 'This quick start demonstrates how to setup a CRUD API through AWS allowing you to create,
list, get, update and delete Todos. DynamoDB is used to store the data.'
layout: Doc
framework: v1
platform: AWS
language: Python
-->
# Serverless CRUD API
This quick start deploys a [CRUD API](https://rapidapi.com/blog/api-glossary/crud/) where you can create, read, update, delete, and list objects stored in a todos table. DynamoDB is used to store the data through AWS.

This service has a src directory for all the CRUD API functions deployed through Lambda. For each operation exactly one file exists e.g. `src/update.py`. In each of these files, the function validates the input and
sends back a response based on the request.

This quick start is based on serverless framework's REST API [Serverless REST API with DynamoDB Tutorial](https://github.com/serverless/examples/tree/master/aws-python-rest-api-with-dynamodb).

## AWS Services

This quick start uses the following AWS services to deploy the CRUD API:

- Deployment: CloudFormation
- Storage: DynamoDB
- API: API Gateway
- Functions: Lambda
- Privileges: IAM

![CRUD-API-Diagram]()

### CloudFormation

CloudFormation is a service that allows you to deploy your project's infrastructure in the AWS
environment all as code. Using CloudFormation, you are able to centralize your project in one area where you
can continually monitor the resources provisioned, events of your project, and more!

In this quick start, CloudFormation uses the `serverless.yml` file to provision all of the functions
and resources in AWS.

### DynamoDB

DynamoDB is a serverless key-valued pair database service that allows you to persistently store information in.
This service is a fully managed, multi-region, durable database with built-in security, backup, and in-memory caching.

In this quick start, you provision a DynamoDB table using the `serverless.yml` file in the `resources` section.
When you create it, you state the provisioned throughput capacity you want to reserve for reads and writes. DynamoDB then reserves the resources to meet your throughput needs.

To change the provisioned throughput, you can edit these configurations via settings in the `serverless.yml`.

```yaml
  ProvisionedThroughput:
    ReadCapacityUnits: 1
    WriteCapacityUnits: 1
```

### Lambda

AWS Lambda is a serverless compute function that allows you to quickly provision new functions in your
environment to automate different tasks. By default, AWS Lambda limits the total concurrent executions across all functions within a given region to 100. The default limit is a safety limit that protects you from costs due to potential runaway or recursive functions during initial development and testing.

To increase this limit above the default, follow the steps in [To request a limit increase for concurrent executions](http://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html#increase-concurrent-executions-limit).

### API Gateway

API Gateway is a service for creating, publishing, and maintaining secure APIs at any scale. When w
you provision your functions, they have an event pathway through API gateway for you to call them.

Example:
```yaml
    events:
      - http:
          path: /v1/todo
          method: POST
          cors: true
```

Using this path, you can change the endpoint API gateway provisions for you functions. CORS is short for
cross origin resource sharing, where other services outside of AWS can also access this endpoint.

### IAM

IAM is a service that enables you to manage access to AWS services and resources securely. By default,
all services and resources provisioned have no privileges to ensure that they do not compromise different parts
of your environment. Therefore, to allow our functions to communicate with DynamoDB, we provision a
role in `serverless.yml`.

```yaml
iamRoleStatements:
  - Effect: "Allow"
    Action:
      - dynamodb:Query
      - dynamodb:PutItem
      - dynamodb:Scan
      - dynamodb:GetItem
      - dynamodb:UpdateItem
      - dynamodb:DeleteItem
    Resource: "arn:aws:dynamodb:${opt:region, self:provider.region}:*:table/${self:provider.environment.DYNAMODB_TABLE}"
```

AWS recommends you to follow the principle of least privilege where a service or user only has the
roles necessary to function. In this quick start, you can break this IAM role down further to only allow
the necessary privileges to each function.

## Setup

```bash
npm install -g serverless
```

## Deploy

In order to deploy the endpoint, you will need to run

```bash
sls deploy
```

The expected result should be similar to:

```bash
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service serverless-crud-api.zip file to S3 (87.98 KB)...
Serverless: Uploading custom CloudFormation resources...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
........................................
Serverless: Stack update finished...
Service Information
service: serverless-crud-api
stage: dev
region: us-west-2
stack: serverless-crud-api-dev
resources: 47
api keys:
  None
endpoints:
  POST - https://6om2glbet3.execute-api.us-west-2.amazonaws.com/dev/v1/todo
  GET - https://6om2glbet3.execute-api.us-west-2.amazonaws.com/dev/v1/todo
  GET - https://6om2glbet3.execute-api.us-west-2.amazonaws.com/dev/v1/todo/{id}
  PUT - https://6om2glbet3.execute-api.us-west-2.amazonaws.com/dev/v1/todo/{id}
  DELETE - https://6om2glbet3.execute-api.us-west-2.amazonaws.com/dev/v1/todo/{id}
functions:
  create: serverless-crud-api-dev-create
  list: serverless-crud-api-dev-list
  get: serverless-crud-api-dev-get
  update: serverless-crud-api-dev-update
  delete: serverless-crud-api-dev-delete
layers:
  None
```

## Usage

You can create, retrieve, update, or delete todos with the following commands:

### Create a Todo

```bash
curl -X POST https://XXXXXXX.execute-api.us-west-2.amazonaws.com/dev/v1/todo --data '{ "task": "Work on food" }'
```

Example Output:
```bash
"{\"id\": \"7b7739c2-7cad-481b-adc1-1fc48613e326\", \"task\": \"Work on food\", \"checked\": false, \"createdAt\": \"1596407014.4433892\", \"updatedAt\": \"1596407014.4433892\"}"%
```

### List all Todos

```bash
curl https://XXXXXXX.execute-api.us-west-2.amazonaws.com/dev/v1/todo
```

Example output:
```bash
[{"checked": true, "task": "Go on a run", "id": "bea44849-0d13-4252-977e-45cce0864c9c", "updatedAt": 1596406707680}, {"checked": false, "createdAt": "1596405816.8263454", "task": "Do homework", "id": "71aa8b21-5e75-4812-820e-46589029fdcf", "updatedAt": "1596405816.8263454"}, {"checked": false, "createdAt": "1596407014.4433892", "task": "Work on food", "id": "7b7739c2-7cad-481b-adc1-1fc48613e326", "updatedAt": "1596407014.4433892"}]%
```

### Get one Todo

```bash
# Replace the <id> part with a real id from your todos table
curl https://XXXXXXX.execute-api.us-west-2.amazonaws.com/dev/v1/todo/<id>
```

Example output:
```bash
{"todo": {"checked": false, "createdAt": "1596405816.8263454", "task": "Do homework", "id": "71aa8b21-5e75-4812-820e-46589029fdcf", "updatedAt": "1596405816.8263454"}}%
```

### Update a Todo

```bash
# Replace the <id> part with a real id from your todos table
curl -X PUT https://XXXXXXX.execute-api.us-west-2.amazonaws.com/dev/v1/todo/71aa8b21-5e75-4812-820e-46589029fdcf --data '{ "task": "Learn serverless", "checked": true }'
```

Example output:
```bash
{"checked": true, "createdAt": "1596405816.8263454", "task": "Learn serverless", "id": "71aa8b21-5e75-4812-820e-46589029fdcf", "updatedAt": 1596407138976}%
```

### Delete a Todo

```bash
# Replace the <id> part with a real id from your todos table
curl -X DELETE https://6om2glbet3.execute-api.us-west-2.amazonaws.com/dev/v1/<id>
```

Example output:
```bash
{"todo": {"ResponseMetadata": {"RequestId": "5VBGHJQ3REQ2T7QRNMO85MHST3VV4KQNSO5AEMVJF66Q9ASUAAJG", "HTTPStatusCode": 200, "HTTPHeaders": {"server": "Server", "date": "Sun, 02 Aug 2020 22:27:14 GMT", "content-type": "application/x-amz-json-1.0", "content-length": "2", "connection": "keep-alive", "x-amzn-requestid": "5VBGHJQ3REQ2T7QRNMO85MHST3VV4KQNSO5AEMVJF66Q9ASUAAJG", "x-amz-crc32": "2745614147"}, "RetryAttempts": 0}}}%  
```
