terraform {
  backend "s3" {
    bucket = "network-tf-state"
    key    = "tf_state"
    region = "us-east-1"
  }
}

module "network_ec2" {
  source = "./network_ec2"
}

module "network_model" {
  source = "./network_model_bucket"
}

module "network_ecr" {
  source = "./network_ecr"
}

module "network_pred_data" {
  source = "./network_pred_data_bucket"
}