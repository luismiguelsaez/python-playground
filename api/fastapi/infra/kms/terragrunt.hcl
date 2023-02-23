terraform {
  source = "git::https://github.com/terraform-aws-modules/terraform-aws-kms//.?ref=v1.3.0"
}

include {
  path   = find_in_parent_folders()
  expose = true
}

############################################################################################
# View all available inputs for this module:
# https://registry.terraform.io/modules/terraform-aws-modules/kms/aws/1.3.0?tab=inputs
############################################################################################

inputs = {
  description             = "KMS key for encrypting volumes of ${include.locals.name} EC2 Instances"
  aliases_use_name_prefix = false
  key_usage               = "ENCRYPT_DECRYPT"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  enable_default_policy = true
}