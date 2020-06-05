import json
import boto3
import time
import os


def get_ssm_data(session):
    client = session.client('ssm')
    response = client.list_compliance_summaries()

    list_ret = []
    for i in response['ComplianceSummaryItems']:
        list_ret.append({
            "ComplianceType": i['ComplianceType'],
            "CompliantCount": str(i['CompliantSummary']['CompliantCount']),
            "NonCompliantCount": str(i['NonCompliantSummary']['NonCompliantCount'])
        })

    return list_ret
