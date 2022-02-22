'''
    Dependency: vpc, security-group
'''
from constructs import Construct
from aws_cdk import Stack, CfnOutput, RemovalPolicy, aws_dynamodb
import json

class DynamoDBStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, project: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # init
        self.project = project
        self.dynamodb = dict()
        
        self.dynamodb['comment'] = aws_dynamodb.Table(self, "dynamodb-comment",
            kinesis_stream=None,
            table_name="comment",
            billing_mode=aws_dynamodb.BillingMode.PROVISIONED,
            contributor_insights_enabled=None,
            encryption=aws_dynamodb.TableEncryption.AWS_MANAGED,
            encryption_key=None,
            point_in_time_recovery=True,
            read_capacity=5,
            write_capacity=5,
            removal_policy=RemovalPolicy.DESTROY,
            replication_regions=None,
            replication_timeout=None,
            stream=None,
            table_class=aws_dynamodb.TableClass.STANDARD,
            time_to_live_attribute=None,
            wait_for_replication_to_finish=None,
            partition_key=aws_dynamodb.Attribute(name="postId",type=aws_dynamodb.AttributeType.STRING),
            sort_key=aws_dynamodb.Attribute(name="commentId",type=aws_dynamodb.AttributeType.STRING))