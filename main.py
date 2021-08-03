#!/usr/bin/env python

import logging
import os
import boto3

from flask import Flask, make_response
from flask_caching import Cache

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

app = Flask(__name__)
cache = Cache(app,config={
        'CACHE_TYPE': 'flask_caching.contrib.uwsgicache.UWSGICache',
        'CACHE_UWSGI_NAME': 'pagecache',
    }
)

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
@cache.cached(timeout=5)
def health_check():

    logger.info("Checking for alarms...")

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

    status_text = PINGDOM_TEMPLATE.format(
        status=status,
        timestamp=timestamp,
    )

    response = make_response(status_text, status_code)
    response.mimetype = "text/xml"
    return response
