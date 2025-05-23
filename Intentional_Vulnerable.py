# Intentionally Vulnerable Terraform Template

provider "aws" {
  region = "us-east-1"
}

# Hardcoded AWS Access Keys (a big no-no!)
provider "aws" {
  access_key = "AKIAEXAMPLEACCESSKEY"
  secret_key = "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY"
}

resource "aws_s3_bucket" "vulnerable_bucket" {
  bucket = "vulnerable-bucket"

  # Misconfigured: Publicly accessible bucket
  acl    = "public-read"

  # Hardcoded sensitive values
  tags = {
    Environment = "dev"
    Password    = "SuperSecretPassword123!"
  }
}

resource "aws_instance" "vulnerable_instance" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"

  # Misconfigured: SSH port wide open to the world
  security_groups = ["open-ssh"]

  user_data = <<-EOF
    #!/bin/bash
    echo "export DB_PASSWORD='HardcodedPassword'" >> /etc/environment
  EOF
}

resource "aws_security_group" "open_ssh" {
  name_prefix = "open-ssh"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"

    # Misconfigured: Wide open to the world
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "vulnerable_module" {
  source = "github.com/example/vulnerable-module?ref=v1.0.0" # Using an outdated and vulnerable module version
}

output "s3_bucket_name" {
  value = aws_s3_bucket.vulnerable_bucket.bucket
}
