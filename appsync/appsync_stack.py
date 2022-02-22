'''
    Dependency: vpc, security-group
'''
from constructs import Construct
from aws_cdk import Stack, CfnOutput, aws_appsync, aws_appsync_alpha, aws_iam
import json

class AppSyncStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, project: dict, database, dynamodb, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # init
        self.project = project
        self.database = database
        self.dynamodb = dynamodb
        self.datasource = dict()
        self.role = dict()
        
        # appsync api
        api = aws_appsync_alpha.GraphqlApi(self, "appsync-foo-api",
            name="foo-api",
            authorization_config=None,
            log_config=aws_appsync_alpha.LogConfig(
                exclude_verbose_content=None,
                field_log_level=aws_appsync_alpha.FieldLogLevel.ALL,
                role=None),
            schema=aws_appsync_alpha.Schema(file_path="appsync/schema.graphql"),
            xray_enabled=None)
        
        # iam policy for aurora serverless data api
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "rds-data:DeleteItems",
                        "rds-data:ExecuteSql",
                        "rds-data:ExecuteStatement",
                        "rds-data:GetItems",
                        "rds-data:InsertItems",
                        "rds-data:UpdateItems"
                    ],
                    "Resource": [
                        f"arn:aws:rds:{self.project['region']}:{self.project['account']}:cluster:{self.database['aurora-mysql-serverless'].cluster_identifier}",
                        f"arn:aws:rds:{self.project['region']}:{self.project['account']}:cluster:{self.database['aurora-mysql-serverless'].cluster_identifier}:*"
                    ]
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "secretsmanager:GetSecretValue"
                    ],
                    "Resource": [
                        f"{self.database['aurora-mysql-serverless'].secret.secret_arn}",
                        f"{self.database['aurora-mysql-serverless'].secret.secret_arn}:*"
                    ]
                }
            ]
        }
        
        # iam role
        self.role['appsync-datasource-rds'] = aws_iam.Role(self, "role-appsync-datasource-rds",
            role_name   = f"{self.project['prefix']}-role-appsync-datasource-rds",
            description = "",
            assumed_by  = aws_iam.ServicePrincipal("appsync.amazonaws.com"),
            inline_policies = {
                "aurora_data_api_policy": aws_iam.PolicyDocument(
                    assign_sids=None,
                    statements=[
                        aws_iam.PolicyStatement.from_json(statement) for statement in policy['Statement']
                    ]),
            })
        
        # appsync datasource to aurora serverless
        self.datasource['relational_database'] = aws_appsync_alpha.BaseDataSource(self, "datasource",
            props=aws_appsync_alpha.BackedDataSourceProps(
                api=api,
                description=None,
                name="aurora-mysql-serverless",
                service_role=self.role['appsync-datasource-rds']),
            type="RELATIONAL_DATABASE",
            dynamo_db_config=None,
            elasticsearch_config=None,
            http_config=None,
            lambda_config=None,
            relational_database_config=aws_appsync.CfnDataSource.RelationalDatabaseConfigProperty(
                relational_database_source_type="RDS_HTTP_ENDPOINT",
                rds_http_endpoint_config=aws_appsync.CfnDataSource.RdsHttpEndpointConfigProperty(
                    aws_region=self.project['region'],
                    aws_secret_store_arn=self.database['aurora-mysql-serverless'].secret.secret_arn,
                    db_cluster_identifier=self.database['aurora-mysql-serverless'].cluster_arn,
                    database_name="db",
                    schema=None)))
        
        # iam policy for dynamodb
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "dynamodb:DeleteItem",
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:Query",
                        "dynamodb:Scan",
                        "dynamodb:UpdateItem"
                    ],
                    "Effect": "Allow",
                    "Resource": [
                        f"arn:aws:dynamodb:{self.project['region']}:{self.project['account']}:table/comment",
                        f"arn:aws:dynamodb:{self.project['region']}:{self.project['account']}:table/comment/*",
                    ]
                }
            ]
        }
        
        # iam role
        self.role['appsync-datasource-ddb'] = aws_iam.Role(self, "role-appsync-datasource-ddb",
            role_name   = f"{self.project['prefix']}-role-appsync-datasource-ddb",
            description = "",
            assumed_by  = aws_iam.ServicePrincipal("appsync.amazonaws.com"),
            inline_policies = {
                "ddb_policy": aws_iam.PolicyDocument(
                    assign_sids=None,
                    statements=[
                        aws_iam.PolicyStatement.from_json(statement) for statement in policy['Statement']
                    ]),
            })
        
        # appsync datasource to dynamodb
        self.datasource['ddb'] = aws_appsync_alpha.BaseDataSource(self, "datasource-ddb",
            props=aws_appsync_alpha.BackedDataSourceProps(
                api=api,
                description=None,
                name="dynamodb",
                service_role=self.role['appsync-datasource-ddb']),
            type="AMAZON_DYNAMODB",
            dynamo_db_config=aws_appsync.CfnDataSource.DynamoDBConfigProperty(
                aws_region=self.project['region'],
                table_name="comment",
                delta_sync_config=None,
                use_caller_credentials=None,
                versioned=None),
            elasticsearch_config=None,
            http_config=None,
            lambda_config=None,
            relational_database_config=None)
        
        # appsync resolver
        api.create_resolver(
            data_source=self.datasource['relational_database'],
            field_name="createPost",
            type_name="Mutation",
            caching_config=None,
            pipeline_config=None,
            request_mapping_template=aws_appsync_alpha.MappingTemplate.from_file("appsync/resolver/post/createPost.req.vtl"),
            response_mapping_template=aws_appsync_alpha.MappingTemplate.from_file("appsync/resolver/post/createPost.res.vtl"))
        
        api.create_resolver(
            data_source=self.datasource['relational_database'],
            field_name="getPost",
            type_name="Query",
            caching_config=None,
            pipeline_config=None,
            request_mapping_template=aws_appsync_alpha.MappingTemplate.from_file("appsync/resolver/post/getPost.req.vtl"),
            response_mapping_template=aws_appsync_alpha.MappingTemplate.from_file("appsync/resolver/post/getPost.res.vtl"))
        
        api.create_resolver(
            data_source=self.datasource['relational_database'],
            field_name="listPost",
            type_name="Query",
            caching_config=None,
            pipeline_config=None,
            request_mapping_template=aws_appsync_alpha.MappingTemplate.from_file("appsync/resolver/post/listPost.req.vtl"),
            response_mapping_template=aws_appsync_alpha.MappingTemplate.from_file("appsync/resolver/post/listPost.res.vtl"))
        
        api.create_resolver(
            data_source=self.datasource['ddb'],
            field_name="createComment",
            type_name="Mutation",
            caching_config=None,
            pipeline_config=None,
            request_mapping_template=aws_appsync_alpha.MappingTemplate.from_file("appsync/resolver/comment/createComment.req.vtl"),
            response_mapping_template=aws_appsync_alpha.MappingTemplate.from_file("appsync/resolver/comment/createComment.res.vtl"))
        
        api.create_resolver(
            data_source=self.datasource['ddb'],
            field_name="listComment",
            type_name="Query",
            caching_config=None,
            pipeline_config=None,
            request_mapping_template=aws_appsync_alpha.MappingTemplate.from_file("appsync/resolver/comment/listComment.req.vtl"),
            response_mapping_template=aws_appsync_alpha.MappingTemplate.from_file("appsync/resolver/comment/listComment.res.vtl"))
        
        # output
        CfnOutput(self, "graphql_url", value=api.graphql_url)
        CfnOutput(self, "api_id", value=api.api_id)
        CfnOutput(self, "api_key", value=api.api_key)