terraform {
  source = "git::https://github.com/terraform-aws-modules/terraform-aws-eks//.?ref=v19.6.0"
}

include {
  path   = find_in_parent_folders()
  expose = true
}

dependency "vpc" {
  config_path                             = "${get_terragrunt_dir()}/../vpc"
  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "terragrunt-info"]
  mock_outputs = {
    vpc_id          = "mocked-vpc-id"
    private_subnets = ["10.0.0.0/16", "10.1.0.0/16"]
  }
}

############################################################################################
# View all available inputs for this module:
# https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/19.6.0?tab=inputs
############################################################################################

inputs = {
  cluster_name    = include.locals.name
  cluster_version = "1.24"

  cluster_endpoint_private_access = true
  # Enabling public endpoint this time, but it must be limited to internal networks, from VPN for example
  cluster_endpoint_public_access  = true

  vpc_id                   = dependency.vpc.outputs.vpc_id
  subnet_ids               = dependency.vpc.outputs.private_subnets

  # Enabling encryption of k8s secrets
  create_kms_key = true

  cluster_encryption_config = {
    resources = ["secrets"]
  }

  kms_key_deletion_window_in_days = 7
  enable_kms_key_rotation         = true
  enable_default_policy           = false

  create_cluster_security_group = true

  cluster_security_group_additional_rules = {}

  manage_aws_auth_configmap = false
}
