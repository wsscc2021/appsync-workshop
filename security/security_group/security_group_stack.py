'''
    Dependncy: VpcStack
'''
from constructs import Construct
from aws_cdk import Stack, Tags, aws_ec2

class SecurityGroupStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, project: dict, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Init
        self.vpc = vpc
        self.project = project
        self.security_group = dict()
        # Security Group
        self.add_security_group(
            name = "aurora",
            description = "",
            allow_all_outbound = False)
            
    '''
        This function create security group, It also tagging for operate efficient.
    '''
    def add_security_group(self, name: str, description: str, allow_all_outbound: bool):
        self.security_group[name] = aws_ec2.SecurityGroup(self, name,
            vpc                 = self.vpc,
            security_group_name = f"{self.project['prefix']}-{name}-sg",
            description         = description,
            allow_all_outbound  = allow_all_outbound)
        Tags.of(self.security_group[name]).add(
            "Name",
            f"{self.project['prefix']}-{name}-sg")