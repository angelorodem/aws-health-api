import boto3
import multiprocessing

class SSM():

    def run(self, region):
        queue = multiprocessing.Queue()
        return (multiprocessing.Process(target=self.__parse_data, args=(queue,region,)), queue)

    def __parse_data(self, queue, region):

        session = boto3
        if region is not None:
            session = boto3.session.Session(region_name=region)      

        client = session.client('ssm')
        response = client.list_compliance_summaries()

        return_dicts = []
        for i in response['ComplianceSummaryItems']:
            return_dicts.append({
                "ComplianceType": i['ComplianceType'],
                "CompliantCount": str(i['CompliantSummary']['CompliantCount']),
                "NonCompliantCount": str(i['NonCompliantSummary']['NonCompliantCount'])
            })

        queue.put({"SSM":return_dicts})
