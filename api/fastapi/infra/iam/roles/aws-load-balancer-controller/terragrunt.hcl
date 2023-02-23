terraform {
  source = "git::https://github.com/terraform-aws-modules/terraform-aws-iam.git//modules/iam-assumable-role-with-oidc?ref=v5.11.2"
}

include {
  path   = find_in_parent_folders()
  expose = true
}

dependency "eks" {
  config_path                             = "${get_terragrunt_dir()}/../../../eks"
  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "terragrunt-info"]
  mock_outputs = {
    cluster_oidc_issuer_url = "https://oidc.eks.eu-central-1.amazonaws.com/id/MOCKED"
  }
}

dependency "iam_policy" {
  config_path                             = "${get_terragrunt_dir()}/../../../iam/policies/aws-load-balancer-controller"
  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "terragrunt-info"]
  mock_outputs = {
    arn = "arn:aws:iam::1234567890:policy/mock-policy-name"
  }
}

################################################################################################################################
# View all available inputs for this module:
# https://registry.terraform.io/modules/terraform-aws-modules/iam/aws/5.11.2/submodules/iam-assumable-role-with-oidc?tab=inputs
################################################################################################################################

inputs = {

  create_role = true

  role_name = "${include.locals.name}-aws-load-balancer-controller@kube-system"

  provider_url = dependency.eks.outputs.cluster_oidc_issuer_url

  role_policy_arns = [
    dependency.iam_policy.outputs.arn
  ]

  number_of_role_policy_arns = 1
}
