import json
import boto3
import time
import os

def get_rds_data(session):
    client = session.client('rds')

    response = client.describe_db_instances()

    list_ret = []
    for i in response['DBInstances']:
        list_ret.append({
            'DBInstanceIdentifier': i['DBInstanceIdentifier'],
            'AllocatedStorage': i['AllocatedStorage'],
            'MaxAllocatedStorage': i['MaxAllocatedStorage'] if 'MaxAllocatedStorage' in i else None,
            'DBInstanceStatus' : i['DBInstanceStatus'],
            'Engine': i['Engine'],
            'SubnetStatus' : [],
        })

        for j in i['DBSubnetGroup']['Subnets']:
            list_ret[-1]['SubnetStatus'].append(j['SubnetStatus'])

    return list_ret


