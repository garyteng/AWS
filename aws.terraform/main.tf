# Refernece

# Terraform tutorial
# [1] http://2ninjas1blog.com/terraform-101-what-is-it-how-do-i-use-it/

# Using existing key
# [2] http://2ninjas1blog.com/terraform-assigning-an-aws-key-pair-to-your-ec2-instance-resource/

# Specify the provider and access details
provider "aws" {
  region = "${var.aws_region}"
}


resource "aws_volume_attachment" "ebs_att" {
  device_name = "/dev/sdf"
  volume_id   = "${aws_ebs_volume.example.id}"
  instance_id = "${aws_instance.web.id}"
}

resource "aws_ebs_volume" "example" {
  availability_zone = "${aws_instance.web.availability_zone}" # "us-west-2a"
  size              = 1
  tags {
        Name = "Terraform Volume"
    }
}

resource "aws_instance" "web" {
  instance_type   = "t2.micro"
  # ami           = "${lookup(var.aws_amis, var.aws_region)}"
  ami             = "ami-07b4f3c02c7f83d59"
  availability_zone = "us-west-2a"

  key_name = "${var.aws_keypair}"

  # Open 22 & 80 Port
  vpc_security_group_ids = ["${aws_security_group.default.id}"]
  subnet_id = "${aws_subnet.default.id}"

  # This will create 1 instances
  count = 1

  # The connection block tells our provisioner how to
  # communicate with the resource (instance)
  connection {
    # The default username for our AMI
    user = "ubuntu"
    host = "${self.public_ip}"
    # The connection will use the local SSH agent for authentication.
    private_key = "${file(var.public_key_path)}"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get -y update", # Take a long time 
      "sudo apt-get -y install nginx",
      "sudo service nginx start",
      "cat /proc/partitions",
      "lsblk",
      "sudo ln -s /dev/xvdf /dev/sdf",
      "sudo file -s /dev/sdf",
      "sudo file -s /dev/xvdf",
      "sudo mke2fs -t ext4 -F -j /dev/sdf",
      "sudo mkdir /mnt/vol_1",
      "sudo mount /dev/sdf /mnt/vol_1",
      "df -T",
      "cd /mnt/vol_1",
      "sudo chmod 777 .",
      "echo \"Hello, world!\" >> greetings.txt",
    ]
  }

  tags = {
    Name = "Terraform Instance!!"
  }

}

# Create a VPC to launch our instances into
resource "aws_vpc" "default" {
  cidr_block = "10.0.0.0/16"
}

# Create an internet gateway to give our subnet access to the outside world
resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.default.id}"
}

# Grant the VPC internet access on its main route table
resource "aws_route" "internet_access" {
  route_table_id         = "${aws_vpc.default.main_route_table_id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.default.id}"
}

# Create a subnet to launch our instances into
resource "aws_subnet" "default" {
  vpc_id                  = "${aws_vpc.default.id}"
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

# Our default security group to access
# the instances over SSH and HTTP
resource "aws_security_group" "default" {
  name        = "terraform_example"
  description = "Used in the terraform"
  vpc_id      = "${aws_vpc.default.id}"

  # SSH access from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP access from the VPC
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # outbound internet access
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}




