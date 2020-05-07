mandar no endpoint um GET com
[todo]


BASE

    {
    	"instancias":	-JSON INSTANCIAS-
    	"compliance": 	-JSON COMPLIANCE-
    	"cache": 		-JSON CACHE-
    	"rds":			-JSON RDS-
    	"beanstalk":	-JSON BEANSTALK-
    }


## -JSON INSTANCIAS-

    "instancias": {
    	"Nome Instancia":{
    		"instance_id": String
    		"projeto": String | null,
    		"sub-projeto": String | null,
    		"instance_state": String,
    		"system_status":[String],
    		"instance_status":[String]
    	}
    }


**Nome Instancia**:   Nome da instancia  
**instance_id**:      id da instancia  
**projeto**           Nome do Projeto Eg. GDOOR-WEB  
**sub-projeto**:		  Nome do sub-projeto Eg. HOMOLOG  
**instance_state** :	'pending'|'running'|'shutting-down'|'terminated'|'stopping'|'stopped'  
**instance_status**:	'passed'|'failed'|'insufficient-data'|'initializing'  
**system_status**:		'passed'|'failed'|'insufficient-data'|'initializing'  



## -JSON COMPLIANCE-

    "compliance":{
    	"Nome Compliance":{
    		"compliant": int,
    		"non-compliant": int
    	}
    },


**"Nome Compliance"**:	Nome da compliance Eg. Patch  
**compliant**:		Numero de maquinas em compliance  
**non-compliant**:	Numero de maquinas fora de compliance  

## -JSON CACHE-

    "cache":{
    	"updates":[
    		{
    			"tipo": String,
    			"grupo_afetado": String,
    			"severidade": String,
    			"status":String,
    			"aplicar_antes_de_utc": int,
    			"sla_atingido": String,
    		}
    	],
    	"grupo_clusters":{
    		"Nome grupo":{
    			"status_grupo":String,
    			"numero_nodes": int
    		}
    	}
    },



**tipo**:					tipo de update,  
**grupo_afetado**:		grupo afetado pela update  
**severidade**:			Severidade da update - 'critical'|'important'|'medium'|'low',  
**status**:				Status da update - 'not-applied'|'waiting-to-start'|'in-progress'|'stopping'|'stopped'|'complete',  
**aplicar_antes_de_utc**: Tempo em unix timestamp  
**sla_atingido**: 		string que indica se a update foi aplicada antes do "aplicar antes de"  - yes'|'no'|'n/a'  
**Nome grupo**:			Nome do grupo  
**status_grupo**:			Status do grupo - available , creating , deleted , deleting , incompatible-network , modifying , rebooting cluster nodes , restore-failed , or snapshotting .  
**numero_nodes**:			Numero de nodes no grupo de cache  


## -JSON RDS-

    "rds":{
    	"Nome database":{
    		"armazenamento_alocado":int,
    		"armazenamento_maximo":int | null,
    		"status": String,
    		"engine": String,
    		"status_subnets":[
    			String
    		]
    	},
    },

**Nome database**: Nome do RDS  
**armazenamento_alocado**:	Numero GB usados do banco  
**armazenamento_maximo**:		Numero maximo de GB a serem usados pelo banco, pode ser null  
**status**: String,			Status do banco - Status possiveis: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.DBInstance.Status.html  
**engine**: String,			Engine usada no banco de dados  
**status_subnets**:			Status das redes do Banco de dados - "Active" (não encontrei os outros estados possiveis)  


## -JSON BEANSTALK-

    "beanstalk":{
    	"nome da aplicação":{
    		"nome do environment":{
    			"instancias":{
    				"identificador instancia":{
    					"status":				String
    					"cor":					String
    					"causas":  			   [String]
    					"metrica_disponivel":	Boolean
    					"metrica_duracao":		int | null
    					"metrica_requests":		int | null
    					"metrica_codigos": {	dict | null
    						"Status2xx":		int		
    						"Status3xx":		int
    						"Status4xx":		int
    						"Status5xx":		int
    					}
    					"metrica_latencia":		int | null,
    					"metrica_cpu":			dict | null
    					 {
    						"User":				float,			
    						"Nice":				float,
    						"System":			float,
    						"Idle":				float,
    						"IOWait":			float,
    						"IRQ":				float,
    						"SoftIRQ":			float
    					 },
    					"metrica_carga":[		dict | null
    					 int
    					],
    					"versao_aplicacao":		String,
    					"deploy_status":		String
    					},
    				},
    				"versao_aplicativo":		String,
    				"status":					String,
    				"cor":						String,
    				"status_saude":				String,
    				"metrica_disponivel":		Boolean,
    				"metrica_latencia":{		dict | null
    				   "P999":				float
    				   "P99":				float
    				   "P95":				float
    				   "P90":				float
    				   "P85":				float
    				   "P75":				float
    				   "P50":				float
    				   "P10":				float
    				},
    				"metrica_duracao":			int | null,
    				"metrica_requests":			int | null,
    				"metrica_codigos":{			dict | null,
    				   "Status2xx":				int | null,
    				   "Status3xx":				int | null,
    				   "Status4xx":				int | null,
    				   "Status5xx":				int | null
    				},
    				"mensagens_status":			string | null
    				"status_maquinas_load_balancer":{
    				   "nome maquina":{
    					  "status": String,
    					  "codigo_rasao": String,
    					  "descricao": String
    				   }
    				}
    			}
    		}
    }

**nome da aplicação**:		Nome da aplicação  
**nome do environment**:		Nome do ambiente onde o código está  
**identificador instancia**:	Identificador das instancias do ambiente  
**status**:				Status da maquina - https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-enhanced-status.html		
**cor**:					Cor referente ao status da maquina - https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-enhanced-status.html  
**causas**:				Mensagem explicando o status da maquina  
**metrica_disponivel**:	Booleano indicando se os valores com metrica_ DESSA MAQUINA estão disponíveis  
**metrica_duracao**:		Periodo de atualização entre metricas  
**metrica_requests**:		Quantidade de requests no periodo de metrica  
**metrica_codigos**:		lista códigos http retornados pela aplicação  
**metrica_latencia**:		Lista contendo 8 metricas de percentil da latência 0.1%(99.9) 1%(99) 5%(95) 10%(90) 15%(85) 25%(75) 50%(50) 90%(10)  
**metrica_cpu**:			lista contendo metrica de uso de CPU em varios niveis (dependente da plataforma pode variar estrutura)  
**metrica_carga**:[[int]]	Lista unitária contendo lista de carga média de cpu para 1 5 e 15 minutos   
**versao_aplicacao**:		Versão do aplicativo q está instalado nessa maquina  
**deploy_status**:		Status de deploy, indica o estado atual de atualizações e modificações "In Progress", Deployed, "Failed"  
**versao_aplicativo**:		Versão do aplicativo que foi colocado no ambiente  
**status**:					Status discritivo do ambiente - 'Launching'|'Updating'|'Ready'|'Terminating'|'Terminated',  
**cor**:						Cor referente ao status do ambiente - 'Green'|'Yellow'|'Red'|'Grey', https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-enhanced-status.html	 
**status_saude**:				Status generico do ambiente - 'NoData'|'Unknown'|'Pending'|'Ok'|'Info'|'Warning'|'Degraded'|'Severe'|'Suspended', https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-enhanced-status.html	  
**metrica_disponivel**:		Booleano indicando se os valores com metrica_ DO AMBIENTE estão disponíveis  
**metrica_latencia**:			Lista contendo 8 metricas de percentil da latência 0.1%(99.9) 1%(99) 5%(95) 10%(90) 15%(85) 25%(75) 50%(50) 90%(10) do AMBIENTE  
**metrica_duracao**:			Periodo de atualização entre metricas  
**metrica_requests**:			Quantidade de requests no periodo de metrica  
**metrica_codigos**:			lista códigos http retornados pela aplicação  
**mensagens_status**:			String informando de forma descritiva os problemas do ambiente (caso tenha)  
**status_maquinas_load_balancer**: Lista de status de comunicação Loadbalancer até a maquina (não funcionando propriamente)  
**nome maquina**:				id da maquina   
**status**: ,					status de conexão com maquina - InService | OutOfService | Unknown  
**codigo_rasao**: ,			em caso de problema qual é o codigo do problema - ELB | Instance | N/A  
**descricao**: 				descrição do problema  



