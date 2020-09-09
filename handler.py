import json
import boto3
import time
import os

from beanstalk import Beanstalk
from ec2 import EC2
from elasticache import Elasticache
from rds import RDS
from ssm import SSM
from ses import SES

from module import read_all,start_all,wait_all

from pprint import pprint

import traceback

def get_values(event):
    region = None
    if 'region' in event:
        region = event['region']

    modules_process = []
    
    if 'custom' not in event:
        beanstalk = Beanstalk()
        modules_process.append(beanstalk.run(region))

        ec2 = EC2()
        modules_process.append(ec2.run(region))

        rds = RDS()
        modules_process.append(rds.run(region))

        ssm = SSM()
        modules_process.append(ssm.run(region))

        ses = SES()
        modules_process.append(ses.run(region))

        elasticache = Elasticache()
        modules_process.append(elasticache.run(region))
    else:
        data = str(event['custom'])

        if 'BEANSTALK' in data:
            beanstalk = Beanstalk()
            modules_process.append(beanstalk.run(region))

        if 'INSTANCES' in data:
            ec2 = EC2()
            modules_process.append(ec2.run(region))

        if 'SSM' in data:
            ssm = SSM()
            modules_process.append(ssm.run(region))

        if 'ELASTICACHE' in data:
            elasticache = Elasticache()
            modules_process.append(elasticache.run(region))

        if 'RDS' in data:
            rds = RDS()
            modules_process.append(rds.run(region))

        if 'SES' in data:
            ses = SES()
            modules_process.append(ses.run(region))


    start_all(modules_process)
    wait_all(modules_process)
    ret_dict = read_all(modules_process)

    return ret_dict


def lambda_handler(event, context):   
    try:
        parameters = ""
        if 'queryStringParameters' in event:
            parameters = event['queryStringParameters']
        else:
            return {
                'statusCode': 401,
                'body': 'Authentication missing'
            }

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

        return {
            'statusCode': 200,
            'body': json.dumps(ret_dict)
        }
    except Exception as e:
        print(traceback.format_exc())
        print(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Internal error')
        }

if __name__ == '__main__':
    os.environ["key"] = ""
    lambda_handler({"queryStringParameters": {"key":""}},[])