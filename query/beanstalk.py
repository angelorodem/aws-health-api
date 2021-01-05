import sys, os
import boto3
import multiprocessing

class Beanstalk():
    def run(self, region):
        queue = multiprocessing.Queue()
        return (multiprocessing.Process(target=self.__parse_data, args=(queue,region,)), queue)

    def __parse_data(self, queue, region):
        
        session = boto3
        if region is not None:
            session = boto3.session.Session(region_name=region)            

        client = session.client('elasticbeanstalk')
        client_elb = session.client('elb')

        applications = client.describe_applications()

        return_dicts = []

        for aplication in applications['Applications']:
            aplication_name = aplication['ApplicationName']

            environments = client.describe_environments(
                ApplicationName= aplication_name,
                IncludeDeleted = True
            )

            for environment in environments['Environments']:
                environment_name = environment['EnvironmentName']
                environment_id = environment['EnvironmentId']
                versao = environment['VersionLabel']
                environment_status = environment['Status']
                cor_saude = environment['Health']
                status_saude = environment['HealthStatus']

                load_balancer_name = None
                resources = client.describe_environment_resources(
                    EnvironmentId=environment_id,
                    EnvironmentName=environment_name
                )
                if 'LoadBalancers' in resources['EnvironmentResources'] and len(resources['EnvironmentResources']['LoadBalancers']) > 0:
                    load_balancer_name = resources['EnvironmentResources']['LoadBalancers'][0]['Name']

                health = client.describe_environment_health(
                    EnvironmentName=environment_name,
                    EnvironmentId=environment_id,
                    AttributeNames=['All']
                )

                metrica_disponivel = True
                metrica_requests = metrica_latencia = metrica_duracao = metrica_codigos = None
                try:
                    metrica_requests = health['ApplicationMetrics']['RequestCount']
                    metrica_latencia = health['ApplicationMetrics']['Latency']
                    metrica_duracao = health['ApplicationMetrics']['Duration']
                    metrica_codigos = health['ApplicationMetrics']['StatusCodes']
                except:
                    metrica_disponivel = False

                mensagens = health['Causes']

                instances_health = client.describe_instances_health(
                    EnvironmentName=environment_name,
                    EnvironmentId=environment_id,
                    AttributeNames=[
                        'All'
                    ]
                )

                instancias = []
                for instance in instances_health['InstanceHealthList']:

                    mdispo = True
                    mdur = mreqs = mcods = mlats = None
                    try:
                        mdur = instance['ApplicationMetrics']['Duration']
                        mreqs = instance['ApplicationMetrics']['RequestCount']
                        mcods = instance['ApplicationMetrics']['StatusCodes']
                        mlats = instance['ApplicationMetrics']['Latency']
                    except:
                        mdispo = False

                    try:
                        mcpus = instance['System']['CPUUtilization']
                        mcarg = instance['System']['LoadAverage']
                    except:
                        mcpus = None
                        mcarg = None

                    instancias.append({
                        'InstanceId': instance['InstanceId'],
                        'HealthStatus': instance['HealthStatus'],
                        'Color': instance['Color'],
                        'Causes': instance['Causes'],
                        'MeticsAvailable': mdispo,
                        'DurationMetric': mdur,
                        'RequestCountMetrics': mreqs,
                        'StatusCodesMetrics': mcods,
                        'LatencyMetrics': mlats,
                        'CPUUtilizationMetrics': mcpus,
                        'LoadAverageMetrics': mcarg,
                        'DeployVersionLabel': instance['Deployment']['VersionLabel'],
                        'DeployStatus': instance['Deployment']['Status']
                    })


                if load_balancer_name is not None and len(load_balancer_name) < 32:

                    elbs = client_elb.describe_instance_health(LoadBalancerName=load_balancer_name)
                    status_maquinas_elb = []
                    for maq in elbs['InstanceStates']:
                        status_maquinas_elb.append({
                            'LoadBalancerInstanceId' : maq['InstanceId'],
                            'LoadBalancerState': maq['State'],
                            'LoadBalancerReasonCode': maq['ReasonCode'],
                            'LoadBalancerDescription': maq['Description'],
                        })

                return_dicts.append({
                    'ApplicationName': aplication_name,
                    'EnvironmentName': environment_name,
                    'EnvironmentInstances': instancias,
                    'EnvironmentVersionLabel': versao,
                    'EnvironmentStatus': environment_status,
                    'EnvironmentColor': cor_saude,
                    'EnvironmentHealthStatus': status_saude,
                    'EnvironmentMetricsAvailable': metrica_disponivel,
                    'EnvironmentLatencyMetrics': metrica_latencia,
                    'EnvironmentDurationMetrics': metrica_duracao,
                    'EnvironmentRequestCountMetrics': metrica_requests,
                    'EnvironmentStatusCodesMetrics':  metrica_codigos,
                    'EnvironmentCauseMessage': mensagens if len(mensagens) > 0 else None,
                    'EnvironmentLoadBalancers': status_maquinas_elb if status_maquinas_elb is not None else None
                })
        print("should store")
        sys.stdout.flush()
        queue.put({"BEANSTALK":return_dicts})
        

