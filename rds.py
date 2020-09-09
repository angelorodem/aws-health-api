import boto3
import multiprocessing

class RDS():

    def run(self, region):
        queue = multiprocessing.Queue()
        return (multiprocessing.Process(target=self.__parse_data, args=(queue,region,)), queue)

    def __parse_data(self, queue, region):

        session = boto3
        if region is not None:
            session = boto3.session.Session(region_name=region)      

        client = session.client('rds')

        response = client.describe_db_instances()

        return_dicts = []
        for i in response['DBInstances']:
            return_dicts.append({
                'DBInstanceIdentifier': i['DBInstanceIdentifier'],
                'AllocatedStorage': i['AllocatedStorage'],
                'MaxAllocatedStorage': i['MaxAllocatedStorage'] if 'MaxAllocatedStorage' in i else None,
                'DBInstanceStatus' : i['DBInstanceStatus'],
                'Engine': i['Engine'],
                'SubnetStatus' : [],
            })

            for j in i['DBSubnetGroup']['Subnets']:
                return_dicts[-1]['SubnetStatus'].append(j['SubnetStatus'])

        queue.put({"RDS":return_dicts})




