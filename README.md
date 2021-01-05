This project is a simple API that returns health information from several different AWS services, using only one lambda function.

It is recommended to use authentication with AWS Cognito at the endpoint of this API to avoid information leakage

The current Code expects a GET input called key (`? Key =`) to authenticate with the environment variable, as the key is fixed, the use of https is extremely necessary.

(readme is not fully updated)

## BASE
Json base que contem cada um dos itens analisados.

    {
    	"INSTANCES":	-INSTANCES JSON-
    	"SSM":			-SSM COMPLIANCE JSON-
    	"ELASTICACHE": 	-ELASTICACHE JSON-
    	"RDS":			-RDS JSON-
    	"BEANSTALK":	-ELASTICBEANSTALK JSON-
    	"SES":			-SES JSON-
    }


## -EC2 JSON-
This JSON  contains information about running instances

    {
       "INSTANCES":[
          {
             "InstanceName":"String",
             "InstanceId":"String",
             "ProjectTag":"String | null",
             "SubProjectTag":"String | null",
             "InstanceState":"String",
             "SystemStatus":[
                "String"
             ],
             "InstanceStatus":[
                "String"
             ]
          }
       ]
    }

- **InstanceName**:		Instance name     
- **InstanceId**:				Unique instance ID    
- **ProjectTag**:				Project tag used to separate projects in the AWS account, default is PROJETO    
- **SubProjectTag**:		Sub-project tag used to separate further the elements in the project, default is SUB-PROJETO    
- **InstanceState**:		'pending'|'running'|'shutting-down'|'terminated'|'stopping'|'stopped'   
- **InstanceStatus**:		'passed'|'failed'|'insufficient-data'|'initializing'   
- **SystemStatus**:			'passed'|'failed'|'insufficient-data'|'initializing'   


## -SSM COMPLIANCE JSON-
JSON for all configurated SSM compliaces.

    {
       "SSM":[
          {
             "ComplianceType":"String",
             "CompliantCount":"int",
             "NonCompliantCount":"int"
          }
       ]
    }

**ComplianceType**:	Compliance name, Eg. Patch Compliance.    
**CompliantCount**:		Number of compliant machines.     
**NonCompliantCount**:	Number of non-compliant machines.     


## -ELASTICACHE JSON-
JSON with information about cache servers.

    {
       "ELASTICACHE":{
          "ClusterUpdates":[
             {
                "ServiceUpdateType":"String",
                "GroupId":"String",
                "ServiceUpdateSeverity":"String",
                "UpdateActionStatus":"String",
                "ServiceUpdateRecommendedApplyByDate":"int",
                "SlaMet":"String"
             }
          ],
          "ClusterGroups":[
             {
                "ReplicationGroupId":"String",
                "CacheClusterStatus":"String",
                "NumCacheNodes":"int"
             }
          ]
       }
    }



- **ServiceUpdateType**:				Update type.     
- **GroupId**:									Cluster group that this update is meant for.    
- **ServiceUpdateSeverity**:		Update severity - 'critical'|'important'|'medium'|'low',     
- **UpdateActionStatus**:				Update status - 'not-applied'|'waiting-to-start'|'in-progress'|'stopping'|'stopped'|'complete',   
- **ServiceUpdateRecommendedApplyByDate**: Tempo em unix timestamp   
- **SlaMet**: 									Update SLA (if it was applied before the recommended date)  - yes'|'no'|'n/a'   
- **ReplicationGroupId**:				Replication group id    
- **CacheClusterStatus**:				Cache cluster status - available , creating , deleted , deleting , incompatible-network , modifying , rebooting cluster nodes , restore-failed , or snapshotting .   
- **NumCacheNodes**:					Number of cache nodes in the cluster     


## -RDS JSON-
JSON containing information about the RDS instances.

    {
       "RDS":[
          {
             "DBInstanceIdentifier":"String",
             "AllocatedStorage":"int",
             "MaxAllocatedStorage":"int | null",
             "DBInstanceStatus":"String",
             "Engine":"String",
             "SubnetStatus":[
                "String"
             ]
          }
       ]
    }

- **DBInstanceIdentifier**: 	RDS DB Instance identifier.    
- **AllocatedStorage**:			Alocated storage for RDS Instance.    
- **MaxAllocatedStorage**:	Max permitted storage.    
- **DBInstanceStatus**: 		Database status - possible statuses:     

| DB Instance Status                  | Description                                                                                                                                                                                                                                                                                                                                                                       |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| available                           | The DB instance is healthy and available.                                                                                                                                                                                                                                                                                                                                         |
| backing-up                          | The DB instance is currently being backed up.                                                                                                                                                                                                                                                                                                                                     |
| backtracking                        | The DB instance is currently being backtracked. This status only applies to Aurora MySQL.                                                                                                                                                                                                                                                                                         |
| configuring-enhanced-monitoring     | Enhanced Monitoring is being enabled or disabled for this DB instance.                                                                                                                                                                                                                                                                                                            |
| configuring-iam-database-auth       | AWS Identity and Access Management (IAM) database authentication is being enabled or disabled for this DB instance.                                                                                                                                                                                                                                                               |
| configuring-log-exports             | Publishing log files to Amazon CloudWatch Logs is being enabled or disabled for this DB instance.                                                                                                                                                                                                                                                                                 |
| converting-to-vpc                   | The DB instance is being converted from a DB instance that is not in an Amazon Virtual Private Cloud (Amazon VPC) to a DB instance that is in an Amazon VPC.                                                                                                                                                                                                                      |
| creating                            | The DB instance is being created. The DB instance is inaccessible while it is being created.                                                                                                                                                                                                                                                                                      |
| deleting                            | The DB instance is being deleted.                                                                                                                                                                                                                                                                                                                                                 |
| failed                              | The DB instance has failed and Amazon RDS can't recover it. Perform a point-in-time restore to the latest restorable time of the DB instance to recover the data.                                                                                                                                                                                                                 |
| inaccessible-encryption-credentials | The AWS KMS key used to encrypt or decrypt the DB instance can't be accessed.                                                                                                                                                                                                                                                                                                     |
| incompatible-network                | Amazon RDS is attempting to perform a recovery action on a DB instance but can't do so because the VPC is in a state that prevents the action from being completed. This status can occur if, for example, all available IP addresses in a subnet are in use and Amazon RDS can't get an IP address for the DB instance.                                                          |
| incompatible-option-group           | Amazon RDS attempted to apply an option group change but can't do so, and Amazon RDS can't roll back to the previous option group state. For more information, check the Recent Events list for the DB instance. This status can occur if, for example, the option group contains an option such as TDE and the DB instance doesn't contain encrypted information.                |
| incompatible-parameters             | Amazon RDS can't start the DB instance because the parameters specified in the DB instance's DB parameter group aren't compatible with the DB instance. Revert the parameter changes or make them compatible with the DB instance to regain access to your DB instance. For more information about the incompatible parameters, check the Recent Events list for the DB instance. |
| incompatible-restore                | Amazon RDS can't do a point-in-time restore. Common causes for this status include using temp tables, using MyISAM tables with MySQL, or using Aria tables with MariaDB.                                                                                                                                                                                                          |
| maintenance                         | Amazon RDS is applying a maintenance update to the DB instance. This status is used for instance-level maintenance that RDS schedules well in advance.                                                                                                                                                                                                                            |
| modifying                           | The DB instance is being modified because of a customer request to modify the DB instance.                                                                                                                                                                                                                                                                                        |
| moving-to-vpc                       | The DB instance is being moved to a new Amazon Virtual Private Cloud (Amazon VPC).                                                                                                                                                                                                                                                                                                |
| rebooting                           | The DB instance is being rebooted because of a customer request or an Amazon RDS process that requires the rebooting of the DB instance.                                                                                                                                                                                                                                          |
| renaming                            | The DB instance is being renamed because of a customer request to rename it.                                                                                                                                                                                                                                                                                                      |
| resetting-master-credentials        | The master credentials for the DB instance are being reset because of a customer request to reset them.                                                                                                                                                                                                                                                                           |
| restore-error                       | The DB instance encountered an error attempting to restore to a point-in-time or from a snapshot.                                                                                                                                                                                                                                                                                 |
| starting                            | The DB instance is starting.                                                                                                                                                                                                                                                                                                                                                      |
| stopped                             | The DB instance is stopped.                                                                                                                                                                                                                                                                                                                                                       |
| stopping                            | The DB instance is being stopped.                                                                                                                                                                                                                                                                                                                                                 |
| storage-full                        | The DB instance has reached its storage capacity allocation. This is a critical status, and we recommend that you fix this issue immediately. To do so, scale up your storage by modifying the DB instance. To avoid this situation, set Amazon CloudWatch alarms to warn you when storage space is getting low.                                                                  |
| storage-optimization                | Your DB instance is being modified to change the storage size or type. The DB instance is fully operational. However, while the status of your DB instance is storage-optimization, you can't request any changes to the storage of your DB instance. The storage optimization process is usually short, but can sometimes take up to and even beyond 24 hours.                   |
| upgrading                           | The database engine version is being upgraded.                                                                                                                                                                                                                                                                                                                                    |
- **Engine**: 							Database Engine.      
- **SubnetStatus**:					Database subnets status (could not find anything other than "available" in AWS Docs)


## -ELASTICBEANSTALK JSON-
JSON that contains elastic beanstalk information.  

     {
        "BEANSTALK":[
           {
              "ApplicationName":"String",
              "EnvironmentName":"String",
              "EnvironmentInstances":[
                 {
                    "InstanceId":"String",
                    "HealthStatus":"String",
                    "Color":"String",
                    "Causes":[
                       "String"
                    ],
                    "MeticsAvailable":"Boolean",
                    "DurationMetric":"int | null",
                    "RequestCountMetrics":"int | null",
                    "StatusCodesMetrics":{
                       "Status2xx":"int",
                       "Status3xx":"int",
                       "Status4xx":"int",
                       "Status5xx":"int"
                    },
                    "LatencyMetrics":"int | null",
                    "CPUUtilizationMetrics":{
                       "User":"float",
                       "Nice":"float",
                       "System":"float",
                       "Idle":"float",
                       "IOWait":"float",
                       "IRQ":"float",
                       "SoftIRQ":"float"
                    },
                    "LoadAverageMetrics":[
                       "int"
                    ],
                    "DeployVersionLabel":"String",
                    "DeployStatus":"String"
                 }
              ],
              "EnvironmentVersionLabel":"String",
              "EnvironmentStatus":"String",
              "EnvironmentColor":"String",
              "EnvironmentHealthStatus":"String",
              "EnvironmentMetricsAvailable":"Boolean",
              "EnvironmentLatencyMetrics":{
                 "P999":"float",
                 "P99":"float",
                 "P95":"float",
                 "P90":"float",
                 "P85":"float",
                 "P75":"float",
                 "P50":"float",
                 "P10":"float"
              },
              "EnvironmentDurationMetrics":"int | null",
              "EnvironmentRequestCountMetrics":"int | null",
              "EnvironmentStatusCodesMetrics":{
                 "Status2xx":"int | null",
                 "Status3xx":"int | null",
                 "Status4xx":"int | null",
                 "Status5xx":"int | null"
              },
              "EnvironmentCauseMessage":"string | null",
              "EnvironmentLoadBalancers":[
                 {
                    "LoadBalancerInstanceId":"String",
                    "LoadBalancerState":"String",
                    "LoadBalancerReasonCode":"String",
                    "LoadBalancerDescription":"String"
                 }
              ]
           }
        ]
     }

   
- **ApplicationName**: Application name    
- **EnvironmentInstances**: List of instances with statuses     

 - **InstanceId**: Identifier of the instances of the environment
 - **HealthStatus**: Machine status - https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-enhanced-status.html    
 - **Color**: Color referring to the status of the machine  https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-enhanced-status.html     
 - **Causes**: Message explaining the status of the machine    
 - **MeticsAvailable**: Boolean indicating whether values ​​with metrica_ OF THIS MACHINE are available       
 - **DurationMetric**: Update period between metrics    
 - **RequestCountMetrics**: Number of requests in the metric period    
 - **StatusCodesMetrics**: lists http codes returned by the application    
 - **LatencyMetrics**: List containing 8 latency percentile metrics 0.1% (99.9) 1% (99) 5% (95) 10% (90) 15%  (85) 25% (75) 50% (50) 90 % (10)    
 - **CPUUtilizationMetrics**: list containing metrics of CPU usage at various levels (depending on the platform, structure may vary)    
 - **LoadAverageMetrics**: [[int]] Unit list containing average load list of cpu for 1 5 and 15 minutes    
 - **DeployVersionLabel**: Version of the application that is installed on this machine    
 - **DeployStatus**: Deployment status, indicates the current status of updates and modifications "In Progress", Deployed, "Failed"    
    
- **EnvironmentName**: Name of the environment where the code is    
- **EnvironmentVersionLabel**: Version of the application that was placed in the environment    
- **EnvironmentStatus**: Discrete environment status - 'Launching' | 'Updating' | 'Ready' | 'Terminating' | 'Terminated',    
- **EnvironmentColor**: Color referring to the status of the environment - 'Green' | 'Yellow' | 'Red' | 'Gray', https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-enhanced -status.html    
- **EnvironmentHealthStatus**: General environment status - 'NoData' | 'Unknown' | 'Pending' | 'Ok' | 'Info' | 'Warning' | 'Degraded' | 'Severe' | 'Suspended', https: / /docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-enhanced-status.html    
- **EnvironmentMetricsAvailable**: Boolean indicating whether values ​​with metrica_ DO AMBIENTE are available    
- **EnvironmentLatencyMetrics**: List containing 8 metrics of latency percentile 0.1% (99.9) 1% (99) 5% (95) 10% (90) 15% (85) 25% (75) 50% (50) 90 % (10) of the ENVIRONMENT    
- **EnvironmentDurationMetrics**: Update period between metrics    
- **EnvironmentRequestCountMetrics**: Number of requests in the metric period    
- **EnvironmentStatusCodesMetrics**: lists http codes returned by the application    
- **EnvironmentCauseMessage**: String informing descriptively the problems of the environment (if any)    
- **EnvironmentLoadBalancers**: Loadbalancer communication status list to the machine (not working properly)    
- **LoadBalancerInstanceId**: machine id    
- **LoadBalancerState**:, machine connection status - InService | OutOfService | Unknown    
- **LoadBalancerReasonCode**:, in case of a problem what is the problem code - ELB | Instance | AT    
- **LoadBalancerDescription**: description of the problem     


## -SES JSON-
    {
        "SES":[
           {
              "StatiticsDataPoints":[
                 {
                    "Timestamp":"datetime(2015, 1, 1)",
                    "DeliveryAttempts":123,
                    "Bounces":123,
                    "Complaints":123,
                    "Rejects":123
                 }
              ],
              "SendingQuota":"int",
              "Domains":"int | null"
           }
        ]
     }

- **StatiticsDataPoints**: lists of graph datapoints containing multiple send statistics   
- **Timestamp**: Timestap of the datapoint    
- **DeliveryAttempts**: numer of delivery attempts     
- **Bounces**: Number of email bounces    
- **Complaints**: Number of email compliants    
- **Rejects**: Number of rejected emails    
- **SendingQuota**: Maximum email sending Quote    
- **Domains**: email domain    

### Roadmap of next features

- ACM
    - Digital certificate status
    - Type (Amazon, Imported)
    - Renewal status
    - Possibility of renewal (Y / n)
    - Certificate expiration date
- AWS Backup
    - Percentage of completion
    - Last plan execution
- CodeBuild
    - Build Status
    - Start / end date time
- ECS
    - Clusters
        - Cluster Status
        - Cluster instance count
        - Cluster pending tasks
        - number of active services
        - Statistics
    - Instance of Containers
        - Same as EC2
    - Services
        - Status
        - Statistics
    - Task
        - Status
        - Health containers
        - Connectivity
- ECR
    - Status scan
    - Scan Results
- AWS Health (Only available in plan)
    - Entities affected by event
    - Status of the entity
    - Event status
    - Event Category
    - Scope of the event
    - Description
    
 #### Distant future
 - S3
 - SQS
 - More SSM
