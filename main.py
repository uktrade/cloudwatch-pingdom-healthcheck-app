#!/usr/bin/env python

import os
import boto3

from flask import Flask
app = Flask(__name__)


PINGDOM_TEMPLATE = """
<pingdom_http_custom_check>
<status>{status}</status>
<response_time>{timestamp}</response_time>
</pingdom_http_custom_check>
"""

ALARM_NAME_PREFIX = os.environ.get("AWS_ALARM_PREFIX", None)
ALARM_NAMES = os.environ["AWS_ALARM_NAMES"].split(",") if "AWS_ALARM_NAMES" in os.environ else None

QUERY_PARAMS = {
    "StateValue": "ALARM",
    "MaxRecords": 100,
}

if ALARM_NAME_PREFIX:
    params["AlarmNamePrefix"] = ALARM_NAME_PREFIX
if ALARM_NAMES:
    params["AlarmNames"] = ALARM_NAMES


@app.route('/')
def health_check():

    client = boto3.client('cloudwatch')
    alarms = client.describe_alarms(**QUERY_PARAMS)

    timestamp = "1"

    if not alarms["MetricAlarms"]:
        status_code = 200
        status = "OK"
    else:
        status_code = 500
        status = "-------------\n".join(
            "\n".join([alarm["AlarmName"], alarm["MetricName"], alarm["StateReason"]])
            for alarm in alarms
        )

    output = PINGDOM_TEMPLATE.format(
        status=status,
        timestamp=timestamp,
    )

    return output, status_code
