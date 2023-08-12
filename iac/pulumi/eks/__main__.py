"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import eks, ec2, iam, get_availability_zones

eks_priv_subnets_num = 3
eks_priv_subnets = []

region_azs = get_availability_zones(state="available")

# Create AWS VPC
eks_vpc = ec2.Vpc(
  'eks-vpc',
  cidr_block='172.18.0.0/16',
  tags={
    "Name": "eks-vpc"
  }
)

for s in range(eks_priv_subnets_num):
  eks_priv_subnets.append(
    ec2.Subnet(
      f'eks-priv-subnet-{s}',
      vpc_id=eks_vpc.id,
      cidr_block=f'172.18.{s}.0/24',
      availability_zone=region_azs.names[s],
      tags={
        "Name": f"eks-priv-subnet-{s}",
        "kubernetes.io/role/internal-elb": "1",
        "az": region_azs.names[s],
        "karpenter.sh/cluster": "true"
      }
    )
  )

eks_iam_role = iam.Role(
  "eks-iam-role",
  assume_role_policy="""{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "eks.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  }""",
  managed_policy_arns=[
    "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  ]
)

eks_security_group = ec2.SecurityGroup(
  "eks-security-group",
  vpc_id=eks_vpc.id,
  description="EKS Security Group",
  ingress=[
    {
      "protocol": "tcp",
      "from_port": 443,
      "to_port": 443,
      "cidr_blocks": ["172.18.0.0/16"],
      "ipv6_cidr_blocks": ["::/0"],
      "description": "Allow pods to communicate with the cluster API Server"
    },
  ],
  egress=[
    {
      "protocol": "-1",
      "from_port": 0,
      "to_port": 0,
      "cidr_blocks": ["0.0.0.0/0"],
      "ipv6_cidr_blocks": ["::/0"],
      "description": "Allow internet access"
    }
  ],
  tags={
    "Name": "eks-security-group"
  }
)

eks_iam_role_nodegroup = iam.Role(
  "eks-iam-role-nodegroup",
  assume_role_policy="""{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  }""",
  managed_policy_arns=[
    "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
    "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  ]
)

eks_cluster = eks.Cluster(
  "eks-cluster",
  version="1.27",
  role_arn=eks_iam_role.arn,
  vpc_config={
    "subnet_ids": [ s.id for s in eks_priv_subnets ],
  },
  enabled_cluster_log_types=[
    "api",
    "audit",
    "authenticator",
    "controllerManager",
    "scheduler",
  ],
  tags={
    "Name": "eks-cluster"
  }
)

eks_cluster_nodegroup = eks.NodeGroup(
  "eks-cluster-nodegroup",
  cluster_name=eks_cluster.name,
  node_group_name="eks-cluster-nodegroup-default",
  node_role_arn=eks_iam_role_nodegroup.arn,
  subnet_ids=[ s.id for s in eks_priv_subnets ],
  scaling_config={
    "desired_size": 3,
    "max_size": 3,
    "min_size": 3,
  },
  instance_types=["t3.medium"],
  ami_type="AL2_x86_64",
)

pulumi.export('eks_cluster_name', eks_cluster.name)
pulumi.export('eks_vpc_id', eks_vpc.id)
