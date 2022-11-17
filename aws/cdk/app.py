
from aws_cdk import (
    aws_ec2 as ec2,
    App, Stack,
)

from constructs import Construct


class EC2InstanceStack(Stack):

  def __init__(self, scope: Construct, id: str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    vpc = ec2.Vpc(self,
      id="VPC",
      ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
      nat_gateways=1,
      max_azs=3,
      subnet_configuration=[
        ec2.SubnetConfiguration(
          name="public",
          subnet_type=ec2.SubnetType.PUBLIC
        ),
        ec2.SubnetConfiguration(
          name="private",
          subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
        )
      ],
    )

    instance_image = ec2.MachineImage.latest_amazon_linux()

    instance = ec2.Instance(self,
      id="testCDK",
      instance_type=ec2.InstanceType("t3.micro"),
      machine_image=instance_image,
      vpc=vpc,
      vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
    )


app = App()

EC2InstanceStack(app, "test")

app.synth()
