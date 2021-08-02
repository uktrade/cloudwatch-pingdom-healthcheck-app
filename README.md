# cloudwatch-pingdom-healthcheck-app

Allow Pingdom to monitor cloudwatch healthchecks from an AWS account

## Configuration

Basic configuration, set the following env vars:\
AWS_ACCESS_KEY_ID\
AWS_SECRET_ACCESS_KEY

This will check for any alarms in the aws account. If no alarms are active you'll see a 200 OK pingdom XML response.  Otherwise details of any active alarms will be reported along with a 500 status code.

You can additionally filter the alarms with the following env vars:

AWS_ALARM_NAMES: supply a comma separated list of alarm names to check\
AWS_ALARM_PREFIX: or supply an alarm name prefix

## TODO:

Add redis for page caching\
Consider p1/p2 split 
