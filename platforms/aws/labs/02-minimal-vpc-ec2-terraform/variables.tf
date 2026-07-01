variable "region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "us-west-2"
}

variable "project" {
  description = "Name prefix / tag applied to every resource."
  type        = string
  default     = "self-cultivation-lab02"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.20.0.0/16"
}

variable "instance_type" {
  description = "EC2 instance type. t3.micro is small and cheap for a lab."
  type        = string
  default     = "t3.micro"
}
