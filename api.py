import json
import boto3
import time
import os


def get_ec2_data():
    ec2 = boto3.resource('ec2')

    dict_ret = {}
    duplicate_names = set()
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

        # Cuida de nomes duplicados
        if instance_name in duplicate_names:
            instance_name = '{} ({})'.format(instance_name, instance_id)

        elif instance_name in dict_ret:
            duplicate_names.add(instance_name)
            temp = dict_ret.pop(instance_name)
            dict_ret['{} ({})'.format(instance_name, temp['id_instancia'])] = temp
            instance_name = '{} ({})'.format(instance_name, instance_id)

        dict_ret[instance_name] = {
            'id_instancia': instance_id,
            'projeto': projeto,
            'sub-projeto': sub_projeto,
            'estado_instancia': instance_state,
            'condicao_sistema': system_status,
            'condicao_instancia': instance_status
        }

    return dict_ret


def get_compliance_data():
    client = boto3.client('ssm')
    response = client.list_compliance_summaries()

    dict_ret = {}
    for i in response['ComplianceSummaryItems']:
        dict_ret[i['ComplianceType']] = {
            "compliant": str(i['CompliantSummary']['CompliantCount']),
            "nao_compliant": str(i['NonCompliantSummary']['NonCompliantCount'])
        }

    return dict_ret


def get_cache_data():
    client = boto3.client('elasticache')

    updates = []

    updates_request = client.describe_update_actions(
        ServiceUpdateStatus=[
            'available', 'cancelled'
        ],
        ShowNodeLevelUpdateStatus=True,
    )
    for j in updates_request['UpdateActions']:
        updates.append({
            'tipo': j['ServiceUpdateType'],
            'grupo_afetado': j['ReplicationGroupId'],
            'severidade': j['ServiceUpdateSeverity'],
            'condicao': j['UpdateActionStatus'],
            'aplicar_antes_de_utc': int(time.mktime(j['ServiceUpdateRecommendedApplyByDate'].timetuple())),
            'sla_atingido': j['SlaMet']
        })

    cluster_request = client.describe_cache_clusters(
        ShowCacheNodeInfo=False
    )

    clusters = {}
    for i in cluster_request['CacheClusters']:
        clusters[i['ReplicationGroupId']] = {
            'status_grupo': i['CacheClusterStatus'],
            'numero_nodes': i['NumCacheNodes']
        }

    upd = {
        "atualizacoes": updates,
        "grupo_clusters": clusters
    }
    return upd


def get_rds_data():
    client = boto3.client('rds')

    response = client.describe_db_instances()

    databases = {}
    for i in response['DBInstances']:
        databases[i['DBInstanceIdentifier']] = {
            'armazenamento_alocado': i['AllocatedStorage'],
            'armazenamento_maximo': i['MaxAllocatedStorage'] if 'MaxAllocatedStorage' in i else None,
            'condicao' : i['DBInstanceStatus'],
            'sgbd': i['Engine'],
            'condicao_subnets' : [],
        }

        for j in i['DBSubnetGroup']['Subnets']:
            databases[i['DBInstanceIdentifier']]['condicao_subnets'].append(j['SubnetStatus'])

    return databases


def get_beanstalk_data():
    client = boto3.client('elasticbeanstalk')
    client_elb = boto3.client('elb')

    applications = client.describe_applications()

    all_beans = {}

    for aplication in applications['Applications']:
        aplication_name = aplication['ApplicationName']
        all_beans[aplication_name] = {}
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

            instancias = {}
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

                instancias[instance['InstanceId']] = {
                    'condicao': instance['HealthStatus'],
                    'cor': instance['Color'],
                    'causas': instance['Causes'],
                    'metrica_disponivel': mdispo,
                    'metrica_duracao': mdur,
                    'metrica_requests': mreqs,
                    'metrica_codigos': mcods,
                    'metrica_latencia': mlats,
                    'metrica_cpu': mcpus,
                    'metrica_carga': mcarg,
                    'versao_aplicacao': instance['Deployment']['VersionLabel'],
                    'condicao_deploy': instance['Deployment']['Status']
                }

            status_maquinas_elb = None
            if load_balancer_name is not None and len(load_balancer_name) < 32:

                elbs = client_elb.describe_instance_health(LoadBalancerName=load_balancer_name)
                status_maquinas_elb = {}
                for maq in elbs['InstanceStates']:
                    status_maquinas_elb[maq['InstanceId']] = {
                        'condicao': maq['State'],
                        'codigo_rasao': maq['ReasonCode'],
                        'descricao': maq['Description'],
                    }

            all_beans[aplication_name][environment_name] = {
                'instancias': instancias,
                'versao_aplicativo': versao,
                'condicao': environment_status,
                'cor': cor_saude,
                'condicao_saude': status_saude,
                'metrica_disponivel': metrica_disponivel,
                'metrica_latencia': metrica_latencia,
                'metrica_duracao': metrica_duracao,
                'metrica_requests': metrica_requests,
                'metrica_codigos':  metrica_codigos,
                'mensagens_condicao': mensagens if len(mensagens) > 0 else None,
                'condicao_maquinas_load_balancer': status_maquinas_elb if status_maquinas_elb is not None else None
            }

    return all_beans


def lambda_handler(event, context):
    try:
        if 'key' not in str(event['queryStringParameters']):
            return {
                'statusCode': 401,
                'body': 'Auth missing'
            }
        else:
            if str(event['queryStringParameters']['key']) != os.environ['key']:
                return {
                    'statusCode': 401,
                    'body': 'Key not valid'
                }

        ret_dict = {'instancias': get_ec2_data(),
                    'compliance': get_compliance_data(),
                    'cache': get_cache_data(),
                    'rds': get_rds_data(),
                    'beanstalk': get_beanstalk_data()}

        print(ret_dict)

        return {
            'statusCode': 200,
            'body': json.dumps(ret_dict)
        }
    except Exception as e:
        # put on cloudwatch logs
        print(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Internal error')
        }
