import json

import pytest

from src import app


@pytest.fixture()
def eventbridge_event():
    """ Generates API GW Event"""

    return {
        {
            "version": "0",
            "id": "6a7e8feb-b491-4cf7-a9f1-bf3703467718",
            "detail-type": "AWS API Call via CloudTrail",
            "source": "aws.ecr",
            "account": "111122223333",
            "time": "2017-12-22T18:43:48Z",
            "region": "eu-central-1",
            "resources": [
                "arn:aws:events:us-east-1:123456789012:rule/ExampleRule"
            ],
            "detail": {
                "requestParameters": {
                    "repositoryName": "test/alpine"
                },
                "eventSource": [
                    "ecr.amazonaws.com"
                ],
                "eventName": [
                    "InitiateLayerUpload"
                ],
                "errorCode": "RepositoryNotFoundException"
            }
        }
    }


def test_lambda_handler(eventbridge_event):

    ret = app.lambda_handler(eventbridge_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "hello world"
