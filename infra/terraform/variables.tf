variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "southamerica-east1"
}

variable "bq_location" {
  type    = string
  default = "US"
}

variable "bucket_name" {
  type = string
}

variable "env" {
  type    = string
  default = "dev"
}
