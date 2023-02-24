data "aws_eks_cluster_auth" "this" {
  name = var.aws_eks_cluster_id
}
