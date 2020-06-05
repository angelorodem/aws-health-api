import json
import boto3
import time
import os

def get_ec2_data(session):
    ec2 = session.resource('ec2')

    list_ret = []
    count = 0
    for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
        instance = ec2.Instance(status['InstanceId'])
        instance_id = status['InstanceId']
        instance_name = "No-Name " + str(count)
        projeto = None
        sub_projeto = None
        count += 1
        for tags in instance.tags:
            if tags["Key"] == 'Name':
                instance_name = tags["Value"]
            if tags["Key"] == 'PROJETO':
                projeto = tags["Value"]
            if tags["Key"] == 'SUB-PROJETO':
                sub_projeto = tags["Value"]

        instance_state = status['InstanceState']['Name']

        instance_status = []
        for i in status['InstanceStatus']['Details']:
            instance_status.append(i['Status'])

        system_status = []
        for i in status['SystemStatus']['Details']:
            system_status.append(i['Status'])

        list_ret.append({
            'InstanceName': instance_name,
            'InstanceId': instance_id,
            'ProjectTag': projeto,
            'SubProjectTag': sub_projeto,
            'InstanceState': instance_state,
            'SystemStatus': system_status,
            'InstanceStatus': instance_status
        })

    return list_ret
