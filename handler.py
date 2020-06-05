import json
import boto3
import time
import os

from beanstalk import get_beanstalk_data
from ec2 import get_ec2_data
from elasticache import get_elasticache_data
from rds import get_rds_data
from ssm import get_ssm_data
from ses import get_ses_data

from pprint import pprint

def get_values(event):
    ret_dict = {}
    #Creates Session
    session = boto3
    if 'region' in event:
        session = boto3.session.Session(region_name=event['region'])

    if "custom" not in event:
        ret_dict['INSTANCES'] = get_ec2_data(session)
        ret_dict['SSM'] = get_ssm_data(session)
        ret_dict['ELASTICACHE'] = get_elasticache_data(session)
        ret_dict['RDS'] = get_rds_data(session)
        ret_dict['BEANSTALK'] = get_beanstalk_data(session)
        ret_dict['SES'] = get_ses_data(session)
    else:
        data = str(event['custom']).split(",")

        if 'INSTANCES' in data:
            ret_dict['INSTANCES'] = get_ec2_data(session)
        if 'SSM' in data:
            ret_dict['SSM'] = get_ssm_data(session)
        if 'ELASTICACHE' in data:
            ret_dict['ELASTICACHE'] = get_elasticache_data(session)
        if 'RDS' in data:
            ret_dict['RDS'] = get_rds_data(session)
        if 'BEANSTALK' in data:
            ret_dict['BEANSTALK'] = get_beanstalk_data(session)
        if 'SES' in data:
            ret_dict['SES'] = get_ses_data(session)

    return ret_dict


def lambda_handler(event, context):
    parameters = event['queryStringParameters']
    try:
        if 'key' not in parameters:
            return {
                'statusCode': 401,
                'body': 'Authentication missing'
            }
        else:
            if str(parameters['key']) !=  os.environ['key']:
                return {
                    'statusCode': 401,
                    'body': 'Key not valid'
                }
                

        ret_dict = get_values(parameters)   

        

        pprint(ret_dict)

        return {
            'statusCode': 200,
            'body': json.dumps(ret_dict)
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Internal error')
        }