import json
import boto3
import datetime
import os

def get_ses_data(session):
    client = session.client('ses')
    clientv2 = session.client('sesv2')

    response_statistics = client.get_send_statistics()

    response_quota = client.get_send_quota()
    del response_quota['ResponseMetadata']

    response_identities = clientv2.list_email_identities()


    domains = []
    for i in response_identities['EmailIdentities']:
        if i['IdentityType'] == 'DOMAIN' or i['IdentityType'] == 'MANAGED_DOMAIN':
            dict_ident = {
                'IdentityName': i['IdentityName'],
                'SendingEnabled': i['SendingEnabled']
            }         
            
            domains.append(dict_ident)


    dict_ret = {
        'StatiticsDataPoints': response_statistics['SendDataPoints'],
        'SendingQuota': response_quota,
        'Domains': domains
    }


    return dict_ret


