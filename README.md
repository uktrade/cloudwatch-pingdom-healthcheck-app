# cloudwatch-pingdom-healthcheck-app

Allow Pingdom to monitor cloudwatch healthchecks from an AWS account

## Configuration

Set the following env vars:\
AWS_ACCESS_KEY_ID\
AWS_SECRET_ACCESS_KEY\
AWS_DEFAULT_REGION

This will check for any alarms in the aws account. If no alarms are active you'll see a 200 OK pingdom XML response.  Otherwise details of any active alarms will be reported along with a 500 status code.

You can additionally filter the alarms with the following env vars:

AWS_ALARM_NAMES: supply a comma separated list of alarm names to check\
AWS_ALARM_PREFIX: or supply an alarm name prefix

## Caching

A 200 response is cached for 5 seconds by default using the uWSGI cache.  This is to limit the queries made to the AWS API.  Note, the dependence on the uWSGI cache means that the app won't run using `flask run` for local development.

## TODO:

Consider p1/p2 split 
