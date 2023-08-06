import re
from slugify import slugify
import dateparser
import boto3
from .exceptions import InvalidArnFormat

def get_jira_id(bn, default):
    # https://community.atlassian.com/t5/Bitbucket-questions/Regex-pattern-to-match-JIRA-issue-key/qaq-p/233319
    m = re.search('(?:[A-Z]{1,10}-?)([A-Z]+-\d+)', bn)
    if m:
        return m.group(0)
    return default

def get_slug(name, max_length=20):
    return slugify(name)[:max_length]

def filter_dateparser(s):
    return dateparser.parse(s)

def filter_format(d, f='%Y-%m-%dT%H:%M:%S.000'):
    # print(d.strftime(f))
    # return "milos"
    
    return str(d.strftime(f))

def _decode_parameter_store_secret(client, arn):
    param = arn.split(':')[5].split('parameter')[1]
    resp = client.get_parameter(Name=param, WithDecryption=True)
    return resp.get("Parameter", {}).get("Value", None)

def decode_aws_secret(arn):
    
    # Kill if not arn
    if arn[:3] != 'arn':
        raise InvalidArnFormat
    
    # Get the 
    a = arn.split(':')
    region = a[3]
    if a[2] == 'ssm':
        client = boto3.client('ssm', region_name=region)
        return _decode_parameter_store_secret(client, arn)

    return arn