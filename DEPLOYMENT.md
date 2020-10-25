# Deployment notes

## Twitter API

For the account that operates the bot, apply for a developer account.

We have a couple of test accounts at the moment:

* [@testbot89629381](https://twitter.com/testbot89629381)
* [@chris48947141](https://twitter.com/chris48947141)

## AWS DynamoDB

The DynamoDB table we've been using is called `scavenged-hate`

The main properties are:

* primary key: `id` (number)
* primary sort key: `created_at` (number)

_NB. If `created_at` isn't stored as a timestamp, we may need to switch the type of the primary sort key to string, or remove it._

### Test table

There is also a table called `test-table` - purely for testing.

The main property is:

* primary key: `id` (string)

## AWS Lambda

We've created an aws lambda function called: `activate-scavenger-bot` (Python 3.8)

### Permissions policy

It runs in a role called: `activate-scavenger-bot-role-gkyu866k`

This role has a permissions policy called `hate-scavenger-bot-lambda-permissions`

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGetItem",
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:Query",
                "dynamodb:UpdateItem",
                "dynamodb:GetRecords"
            ],
            "Resource": [
                "arn:aws:dynamodb:eu-west-2:344780153051:table/scavenged-hate/stream/stream",
                "arn:aws:dynamodb:eu-west-2:344780153051:table/test-table/stream/stream",
                "arn:aws:dynamodb:eu-west-2:344780153051:table/test-table",
                "arn:aws:dynamodb:eu-west-2:344780153051:table/scavenged-hate"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "dynamodb:GetRecords",
            "Resource": [
                "arn:aws:dynamodb:eu-west-2:344780153051:table/test-table/stream/stream",
                "arn:aws:dynamodb:eu-west-2:344780153051:table/scavenged-hate/stream/stream"
            ]
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

### Layers

#### tweepy

A layer called `tweepy-layer` contains the tweepy library for access to the Twitter API.

With this layer applied to the Lambda, we can `import tweepy`.

It was created with:

```bash
mkdir tweepy-layer/python
pip3 install tweepy -t tweepy-layer/python/
cd tweepy-layer/
zip -r tweepy-layer.zip python
```

This zip can then be uploaded to AWS Lambda to create the layer.
