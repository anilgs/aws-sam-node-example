import json
import logging
import boto3
import os
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit

log = logging.getLogger()
log.setLevel(logging.DEBUG)

tablename = os.getenv("TABLE_NAME")

tracer = Tracer(service="Get")
logger = Logger(service="Get")
metrics = Metrics(service="Get", namespace="GetService")


def custom_authorize(event):
    log.debug("Received in custom_authorize: {}".format(json.dumps(event)))
    id = event['pathParameters']['id']
    log.debug("id: {}".format(id))
    try:

        return respond(data=resp, status=200)
    except ClientError as e:
        print(e)
        return respond(data="Operation failed", status=500)

@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler
@logger.inject_lambda_context
def lambda_handler(event, context):

    metrics.add_metric(name="GetSucceeded", value=1, unit=MetricUnit.Count)

    log.debug("Received event in get_item: {}".format(json.dumps(event)))
    return custom_authorize(event)

def respond(data="", status=200):
    return {
        "statusCode": status,
        "body": json.dumps(data)
    }
