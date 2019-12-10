variable "aws_region" {
  description = "The AWS region to create things in."
  default     = "us-west-2"
}

variable "aws_keypair" {
  description = "Name of default key-pair."
  default     = "2019 AWS Class"
}

variable "public_key_path" {
  description = "Example: ~/.ssh/terraform.pub"
  default     = "/home/gary/.aws/2019AWSClass.pem"
}

# Ubuntu 18.04
variable "aws_amis" {
  default = {
    "us-west-2a" = "ami-07b4f3c02c7f83d59"
  }
}

