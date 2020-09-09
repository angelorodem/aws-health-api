import time
import boto3
import multiprocessing

class Elasticache():

    def run(self, region):
        queue = multiprocessing.Queue()
        return (multiprocessing.Process(target=self.__parse_data, args=(queue,region,)), queue)

    def __parse_data(self, queue, region):

        session = boto3
        if region is not None:
            session = boto3.session.Session(region_name=region)     

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

        return_dict = {
            "ClusterUpdates": updates,
            "ClusterGroups": clusters
        }


        queue.put({"ELASTICACHE":return_dict})
 
