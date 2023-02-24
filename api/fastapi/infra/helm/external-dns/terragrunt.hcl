terraform {
  source = "git::https://github.com/cloudposse/terraform-aws-helm-release.git//?ref=0.7.0"
}

include {
  path   = find_in_parent_folders()
  expose = true
}

# Generating helm provider to get the needed credentials
generate "helm-provider" {
  path      = "helm-provider.tf"
  if_exists = "overwrite"
  contents  = <<EOF
provider "helm" {
  kubernetes {
    host                   = "${dependency.eks.outputs.cluster_endpoint}"
    token                  = "${dependency.eks_auth.outputs.token}"
    cluster_ca_certificate = <<-CERT
${base64decode(dependency.eks.outputs.cluster_certificate_authority_data)}
    CERT
  }
}
EOF
}

# Using locally defined module to get EKS auth data
dependency "eks_auth" {
  config_path = "${get_terragrunt_dir()}/../../eks-auth"
  mock_outputs = {
    token = "mocked-token"
  }
}

dependency "eks" {
  config_path                             = "${get_terragrunt_dir()}/../../eks"
  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "terragrunt-info"]
  mock_outputs = {
    cluster_oidc_issuer_url            = "https://oidc.eks.eu-central-1.amazonaws.com/id/MOCKED"
    cluster_endpoint                   = "https://mock-cluster.endpoint.cloud"
    cluster_certificate_authority_data = "cmFuZG9tLWRhdGEK"
  }
}

dependency "iam_role" {
  config_path                             = "${get_terragrunt_dir()}/../../iam/roles/external-dns"
  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "terragrunt-info"]
  mock_outputs = {
    iam_role_arn = "mock-iam-role-arn"
  }
}

#####################################################################################################################
# View all available inputs for this module:
# https://registry.terraform.io/modules/cloudposse/helm-release/aws/0.7.0?tab=inputs
#####################################################################################################################

inputs = {
  name = "external-dns"

  repository    = "https://kubernetes-sigs.github.io/external-dns"
  chart         = "external-dns"
  chart_version = "1.10.1"

  create_namespace     = false
  kubernetes_namespace = "kube-system"

  atomic          = false
  cleanup_on_fail = false
  timeout         = "300"
  wait            = false

  eks_cluster_oidc_issuer_url = dependency.eks.outputs.cluster_oidc_issuer_url

  values = [templatefile("${get_terragrunt_dir()}/files/values.yaml", {
    iam_role_arn = dependency.iam_role.outputs.iam_role_arn
  })]
}
