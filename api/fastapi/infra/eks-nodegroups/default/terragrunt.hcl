terraform {
  source = "git::https://github.com/terraform-aws-modules/terraform-aws-eks.git//modules/eks-managed-node-group?ref=v19.6.0"
}

include {
  path   = find_in_parent_folders()
  expose = true
}

dependency "eks" {
  config_path                             = "${get_terragrunt_dir()}/../../eks"
  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "terragrunt-info"]
  mock_outputs = {
    iam_role_arn                      = "mocked-iam-role-arn"
    cluster_primary_security_group_id = "sg-00000000"
  }
}

dependency "vpc" {
  config_path                             = "${get_terragrunt_dir()}/../../vpc"
  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "terragrunt-info"]
  mock_outputs = {
    vpc_id          = "mocked-vpc-id"
    private_subnets = ["10.0.0.0/16", "10.1.0.0/16"]
  }
}

############################################################################################################################
# View all available inputs for this module:
# https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/19.6.0/submodules/eks-managed-node-group?tab=inputs
############################################################################################################################

inputs = {
  name            = "${include.locals.name}-default"
  cluster_name    = include.locals.name
  use_name_prefix = false
  iam_role_name   = "${include.locals.name}-default-eks-ng"

  create_launch_template      = true
  launch_template_name        = ""
  launch_template_description = "${include.locals.name}-system node group"

  ami_release_version = "1.24.7-20230105"
  platform            = "linux"
  capacity_type       = "ON_DEMAND"
  instance_types      = ["c5a.large", "c6a.large", "c6i.large", "c5.large"]

  disk_size    = 50
  min_size     = 3
  desired_size = 3
  max_size     = 5

  vpc_id     = dependency.vpc.outputs.vpc_id
  subnet_ids = dependency.vpc.outputs.private_subnets

  cluster_primary_security_group_id = dependency.eks.outputs.cluster_primary_security_group_id
  vpc_security_group_ids            = []

  update_config = {
    max_unavailable_percentage = 30
  }

  labels = {
    "role" : "default",
  }

  # Adding taing for Cilium
  taints = [
    {
      key    = "node.cilium.io/agent-not-ready"
      value  = "true"
      effect = "NO_SCHEDULE"
    }
  ]

  disable_api_termination = false
  ebs_optimized           = true
  key_name                = "Platform"
  block_device_mappings = {
    xvda = {
      device_name = "/dev/xvda"
      ebs = {
        volume_size           = 20
        volume_type           = "gp3"
        # Disabling encryption for simplicity. For live environments, KMS key encriptions should be enabled
        encrypted             = false
        delete_on_termination = true
      }
    }
  }
  # Updating metadata, like hop limit for EC2 metadata endpoint to be accessible from containers
  metadata_options = {
    "http_endpoint" : "enabled",
    "http_put_response_hop_limit" : 2,
    "http_tokens" : "required",
    "instance_metadata_tags" : "disabled"
  }
  enable_monitoring = false
  tag_specifications = ["instance"]
  tags = {
    Name = "${include.locals.name}-default"
  }
}