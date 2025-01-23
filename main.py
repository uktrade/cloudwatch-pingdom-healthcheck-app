import logging
import os
import boto3

from flask import Flask, make_response
#from flask_caching import Cache

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

app = Flask(__name__)
# cache = Cache(app,config={
#        'CACHE_TYPE': 'flask_caching.contrib.uwsgicache.UWSGICache',
#        'CACHE_UWSGI_NAME': 'pagecache',
#    }
#)

PINGDOM_TEMPLATE = """
<pingdom_http_custom_check>
    <status>{status}</status>
    <response_time>{timestamp}</response_time>
</pingdom_http_custom_check>
"""

P1_ALARM_NAME_PREFIX = os.environ.get("P1_AWS_ALARM_PREFIX", None)
P1_ALARM_NAMES = os.environ["P1_AWS_ALARM_NAMES"].split(",") if "P1_AWS_ALARM_NAMES" in os.environ else None

P2_ALARM_NAME_PREFIX = os.environ.get("P2_AWS_ALARM_PREFIX", None)
P2_ALARM_NAMES = os.environ["P2_AWS_ALARM_NAMES"].split(",") if "P2_AWS_ALARM_NAMES" in os.environ else None

P1_QUERY_PARAMS = {
    "StateValue": "ALARM",
    "MaxRecords": 100,
}

P2_QUERY_PARAMS = {
    "StateValue": "ALARM",
    "MaxRecords": 100,
}

if P1_ALARM_NAME_PREFIX:
    P1_QUERY_PARAMS["AlarmNamePrefix"] = P1_ALARM_NAME_PREFIX
if P1_ALARM_NAMES:
    P1_QUERY_PARAMS["AlarmNames"] = P1_ALARM_NAMES

if P2_ALARM_NAME_PREFIX:
    P2_QUERY_PARAMS["AlarmNamePrefix"] = P2_ALARM_NAME_PREFIX
if P2_ALARM_NAMES:
    P2_QUERY_PARAMS["AlarmNames"] = P2_ALARM_NAMES


# @app.route('/p1', defaults={'query': P1_QUERY_PARAMS})
# @app.route('/p2', defaults={'query': P2_QUERY_PARAMS})
@app.route('/p1', defaults={'query': P1_QUERY_PARAMS})
#@cache.cached(timeout=5)
def handle_request(query):
    logger.info("Checking for alarms...")

    client = boto3.client('cloudwatch')
    alarms = client.describe_alarms(**query)

    if not alarms["MetricAlarms"]:
        status_code = 200
        status = "OK"
    else:
        status_code = 500
        status = "-------------\n".join(
            "\n  ".join([alarm["AlarmName"], alarm["MetricName"], alarm["StateReason"]])
            for alarm in alarms["MetricAlarms"]
        )

    timestamp = "1"
    status_text = PINGDOM_TEMPLATE.format(
        status=status,
        timestamp=timestamp,
    )

    response = make_response(status_text, status_code)
    response.mimetype = "text/xml"
    return response

@app.route('/pingdom/ping.xml')
def internal_healthcheck():
    response = make_response(PINGDOM_TEMPLATE.format(status="OK", timestamp="1"), 200)
    response.mimetype = "text/xml"
    return response
