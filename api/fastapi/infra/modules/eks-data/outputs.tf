output "token" {
  value = data.aws_eks_cluster_auth.this.token
  sensitive = true
}
