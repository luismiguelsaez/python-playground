terraform {
  source = "git::https://github.com/terraform-aws-modules/terraform-aws-ecr//.?ref=v1.6.0"
}

include {
  path   = find_in_parent_folders()
  expose = true
}

dependency "eks_nodegroup_default" {
  config_path                             = "${get_terragrunt_dir()}/../eks-nodegroups/default"
  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "terragrunt-info"]
  mock_outputs = {
    iam_role_arn = "mocked-iam-role-arn"
  }
}
############################################################################################
# View all available inputs for this module:
# https://registry.terraform.io/modules/terraform-aws-modules/ecr/aws/1.6.0?tab=inputs
############################################################################################

inputs = {

  create            = true
  create_repository = true

  repository_name = "apps/fastapi"
  repository_type = "private"

  create_lifecycle_policy = true
  create_registry_policy  = true

  registry_scan_type            = "BASIC"
  repository_encryption_type    = "AES256"
  repository_image_scan_on_push = true

  repository_read_access_arns       = [ dependency.eks_nodegroup_default.outputs.iam_role_arn ]
  repository_read_write_access_arns = []

  repository_lifecycle_policy = <<EOF
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Expire images exceeding count",
      "selection": {
        "tagStatus": "any",
        "countType": "imageCountMoreThan",
        "countNumber": 20
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
EOF

}
