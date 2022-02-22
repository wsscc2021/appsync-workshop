'''
    Dependency: vpc, security-group
'''
from constructs import Construct
from aws_cdk import CfnOutput, Stack, Duration, RemovalPolicy, aws_iam, aws_kms, aws_ec2, aws_logs, aws_rds

class RdsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, project: dict, vpc, security_group, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Init
        self.vpc = vpc
        self.project = project
        self.security_group = security_group
        self.role = dict()
        self.kms_key = dict()
        self.database = dict()
        
        # subnet group
        self.subnet_group = aws_rds.SubnetGroup(self, "rds-subnetgroup",
            subnet_group_name=f"{self.project['prefix']}-rds-subnetgroup",
            description="vpc's description",
            vpc=self.vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PRIVATE_ISOLATED),
            removal_policy=RemovalPolicy.DESTROY)
        
        # IAM role for cloudwatch to monitoring and logging
        self.role['monitoring'] = aws_iam.Role(self, "rds-monitoring-role",
            role_name   = f"{project['prefix']}-role-rds-monitoring",
            description = "",
            assumed_by  = aws_iam.ServicePrincipal("monitoring.rds.amazonaws.com"),
            external_ids=None,
            inline_policies=None,
            max_session_duration=None,
            path=None,
            permissions_boundary=None,
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonRDSEnhancedMonitoringRole")
            ]
        )
        
        # kms
        self.kms_key['rds'] = aws_kms.Key(self, "cmk-rds",
            alias               = f"alias/{project['prefix']}-rds",
            description         = "",
            admins              = None,
            enabled             = True,
            enable_key_rotation = True,
            pending_window      = Duration.days(7),
            removal_policy      = RemovalPolicy.DESTROY
        )

        # database
        self.add_aurora_mysql_serverless()
    
    def add_aurora_mysql_serverless(self):
        # parameter group
        parameter_group = aws_rds.ParameterGroup(self, "aurora_mysql_parameter_group", 
            engine=aws_rds.DatabaseClusterEngine.aurora_mysql(
                version=aws_rds.AuroraMysqlEngineVersion.VER_2_07_1),
            description="aurora-mysql's paramter-group",
            parameters={
                "max_connections": "1500"
            })
        # serverless cluster
        self.database['aurora-mysql-serverless'] = aws_rds.ServerlessCluster(self, "aurora_mysql_serverless",
            engine=aws_rds.DatabaseClusterEngine.aurora_mysql(
                version=aws_rds.AuroraMysqlEngineVersion.VER_2_07_1),
            vpc=self.vpc,
            backup_retention=None,
            cluster_identifier=f"{self.project['prefix']}-aurora-mysql-serverless",
            credentials=None,
            default_database_name="db",
            deletion_protection=None,
            enable_data_api=True,
            parameter_group=parameter_group,
            removal_policy=RemovalPolicy.DESTROY,
            scaling=None,
            security_groups=[
                self.security_group['aurora']
            ],
            storage_encryption_key=self.kms_key['rds'],
            subnet_group=self.subnet_group,
            vpc_subnets=None
        )
        
        # Output
        CfnOutput(self, f"aurora_mysql_serverless_identifier",
            value=self.database['aurora-mysql-serverless'].cluster_identifier)
        CfnOutput(self, f"aurora_mysql_serverless_endpoint",
            value=self.database['aurora-mysql-serverless'].cluster_endpoint.socket_address)
        CfnOutput(self, f"aurora_mysql_serverless_secrets",
            value=self.database['aurora-mysql-serverless'].secret.secret_name)