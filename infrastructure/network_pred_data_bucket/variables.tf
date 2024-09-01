variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "pred_data_bucket_name" {
  type    = string
  default = "network-datasource"
}

variable "aws_account_id" {
  type    = string
  default = "566373416292"
}

variable "force_destroy_bucket" {
  type    = bool
  default = true
}

