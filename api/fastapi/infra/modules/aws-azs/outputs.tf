output "aws_availability_zones" {
  description = "List of availability zones"
  value       = slice(data.aws_availability_zones.available.names, 0, var.max_az_count)
}
