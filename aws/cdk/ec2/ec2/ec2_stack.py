from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)

from constructs import Construct
from os import environ


class Ec2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        subnets_private = [
            ec2.SubnetConfiguration(name='private_1', subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24),
            ec2.SubnetConfiguration(name='private_2', subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24),
            ec2.SubnetConfiguration(name='private_3', subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24),
        ]

        subnets_public = [
            ec2.SubnetConfiguration(name='public_1', subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
            ec2.SubnetConfiguration(name='public_2', subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
            ec2.SubnetConfiguration(name='public_3', subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
        ]

        vpc = ec2.Vpc(
            self,
            id='vpc',
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=3,
            subnet_configuration=[*subnets_public, *subnets_private]
        )

        with open(environ['HOME'] + '/.ssh/id_rsa.pub') as f:
            pub_key_material = f.readlines()[0]

        key = ec2.CfnKeyPair(self, id='key', key_name='default', public_key_material=pub_key_material)

        instance = ec2.Instance(
            self,
            id='instance',
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3A, ec2.InstanceSize.MEDIUM),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            key_name=key.key_name,
        )
