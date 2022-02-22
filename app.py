#!/usr/bin/env python3
'''
    Initial cdk project information
    1. Import CDK modules
    2. Import Services modules in this project
    3. Project information
    4. cdk Construct
'''
# Import CDK modules
from aws_cdk import App, Environment

# Import Services modules
from vpc.vpc_stack import VpcStack
from security.security_group.security_group_stack import SecurityGroupStack
from rds.rds_stack import RdsStack
from appsync.appsync_stack import AppSyncStack
from dynamodb.dynamodb_stack import DynamoDBStack

# Information of project
project = dict()
project['account'] = "242593025403"
project['region']  = "us-east-1"
project['env']     = "appsync"
project['name']    = "workshop"
project['prefix']  = f"{project['env']}-{project['name']}"

# cdk environment
cdk_environment = Environment(
    account=project['account'],
    region=project['region'])

# cdk construct
app = App()

# VPC
vpc_stack = VpcStack(
    scope        = app,
    construct_id = f"{project['prefix']}",
    env          = cdk_environment,
    project      = project)

security_group_stack = SecurityGroupStack(
    scope        = app,
    env          = cdk_environment,
    construct_id = f"{project['prefix']}-security-group",
    project      = project,
    vpc          = vpc_stack.vpc)

rds_stack = RdsStack(
    scope          = app,
    env            = cdk_environment,
    construct_id   = f"{project['prefix']}-rds",
    project        = project,
    vpc            = vpc_stack.vpc,
    security_group = security_group_stack.security_group)

dynamodb_stack = DynamoDBStack(
    scope          = app,
    env            = cdk_environment,
    construct_id   = f"{project['prefix']}-dynamodb",
    project        = project)

appsync_stack = AppSyncStack(
    scope          = app,
    env            = cdk_environment,
    construct_id   = f"{project['prefix']}-appsync",
    project        = project,
    database       = rds_stack.database,
    dynamodb       = dynamodb_stack.dynamodb)

# app synth -> cloudformation template
app.synth()