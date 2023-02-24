terraform {
  source = "${get_terragrunt_dir()}/../modules/aws-azs"
}

include {
  path   = find_in_parent_folders()
  expose = true
}

inputs = {
  max_az_count = include.locals.az_num
}
