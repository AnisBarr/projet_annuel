provider "aws" {
  region = "eu-west-1"
}


data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "all" {
  vpc_id = data.aws_vpc.default.id
}

data "aws_security_group" "default" {
  vpc_id = data.aws_vpc.default.id
  name   = "default"
}


module "db" {
  
  identifier = "admin"


  engine            = "mysql"
  engine_version    = "5.7.19"
  instance_class    = "db.t2.large"
  allocated_storage = 5
  storage_encrypted = false

  kms_key_id        = "arm:aws:kms:<eu-west-1>: ""  :key ""
  name     = "projetannuel"
  username = "admin"
  password = "adminadmin"
  port     = "3306"

  vpc_security_group_ids = [data.aws_security_group.default.id]

  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window      = "03:00-06:00"

  multi_az = true

  # disable backups to create DB faster
  backup_retention_period = 0

  tags = {
    Owner       = "admin"
    Environment = "dev"
  }

  enabled_cloudwatch_logs_exports = ["audit", "general"]


  subnet_ids = data.aws_subnet_ids.all.ids

  family = "mysql5.7"

  major_engine_version = "5.7"

  final_snapshot_identifier = "projetannuel"

  deletion_protection = false

  parameters = [
    {
      name  = "character_set_client"
      value = "utf8"
    },
    {
      name  = "character_set_server"
      value = "utf8"
    }
  ]

}