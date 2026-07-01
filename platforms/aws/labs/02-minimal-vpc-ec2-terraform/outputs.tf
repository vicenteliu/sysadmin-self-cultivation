output "instance_id" {
  description = "EC2 instance ID."
  value       = aws_instance.app.id
}

output "private_ip" {
  description = "Instance private IP (there is no public IP, by design)."
  value       = aws_instance.app.private_ip
}

output "connect_command" {
  description = "Open a shell via SSM Session Manager — no SSH, no open ports."
  value       = "aws ssm start-session --target ${aws_instance.app.id} --region ${var.region}"
}

output "region" {
  description = "Region the stack was deployed into."
  value       = var.region
}
