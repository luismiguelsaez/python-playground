terraform {
  source = "git::https://github.com/terraform-aws-modules/terraform-aws-vpc.git//?ref=v3.19.0"
}

include {
  path   = find_in_parent_folders()
  expose = true
}

#################################################################################################
# View all available inputs for this module:
# https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/3.19.0?tab=inputs
#################################################################################################

inputs = {
  name            = include.locals.name
  cidr            = include.locals.vpc_cidr
  azs             = include.locals.az_list
  private_subnets = [cidrsubnet(include.locals.vpc_cidr, 2, 2), cidrsubnet(include.locals.vpc_cidr, 2, 3)]
  public_subnets  = [cidrsubnet(include.locals.vpc_cidr, 3, 2), cidrsubnet(include.locals.vpc_cidr, 3, 3)]
  intra_subnets   = [cidrsubnet(include.locals.vpc_cidr, 3, 0), cidrsubnet(include.locals.vpc_cidr, 3, 1)]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true
  enable_dns_support   = true

  enable_flow_log                      = false
  create_flow_log_cloudwatch_iam_role  = false
  create_flow_log_cloudwatch_log_group = false

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }

}
