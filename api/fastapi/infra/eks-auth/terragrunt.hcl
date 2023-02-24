terraform {
  source = "${get_terragrunt_dir()}/../modules/eks-data"
}

dependency "eks" {
  config_path = "${get_terragrunt_dir()}/../eks"
  mock_outputs = {
    cluster_name  = "mocked-eks-cluster-name"
  }
}

inputs = {
  aws_eks_cluster_id = dependency.eks.outputs.cluster_name
}
