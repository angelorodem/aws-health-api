import boto3
import multiprocessing

class SES():

    def run(self, region):
        queue = multiprocessing.Queue()
        return (multiprocessing.Process(target=self.__parse_data, args=(queue,region,)), queue)

    def __parse_data(self, queue, region):

        session = boto3
        if region is not None:
            session = boto3.session.Session(region_name=region)      

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


        return_dict = {
            'StatiticsDataPoints': response_statistics['SendDataPoints'],
            'SendingQuota': response_quota,
            'Domains': domains
        }

        queue.put({"SES":return_dict})
 



