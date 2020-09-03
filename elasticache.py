import json
import boto3
import time
import os


def get_elasticache_data(session):
    client = session.client('elasticache')

    updates = []

    updates_request = client.describe_update_actions(
        ServiceUpdateStatus=[
            'available', 'cancelled'
        ],
        ShowNodeLevelUpdateStatus=True,
    )
    for j in updates_request['UpdateActions']:
        updates.append({
            'ServiceUpdateType': j['ServiceUpdateType'],
            'GroupId': j['ReplicationGroupId'],
            'ServiceUpdateSeverity': j['ServiceUpdateSeverity'],
            'UpdateActionStatus': j['UpdateActionStatus'],
            'ServiceUpdateRecommendedApplyByDate': int(time.mktime(j['ServiceUpdateRecommendedApplyByDate'].timetuple())),
            'SlaMet': j['SlaMet']
        })

    cluster_request = client.describe_cache_clusters(
        ShowCacheNodeInfo=False
    )

    clusters = []
    for i in cluster_request['CacheClusters']:
        clusters.append({
            'ReplicationGroupId':i['ReplicationGroupId'],
            'CacheClusterStatus': i['CacheClusterStatus'],
            'NumCacheNodes': i['NumCacheNodes']
        })

    upd = {
        "ClusterUpdates": updates,
        "ClusterGroups": clusters
    }
    return upd
