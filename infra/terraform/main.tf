terraform {
  required_version = ">= 1.9"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  labels = {
    projeto  = "tech-challenge-alfabetizacao"
    ambiente = var.env
  }
}

resource "google_storage_bucket" "lake" {
  name                        = var.bucket_name
  location                    = var.bq_location
  uniform_bucket_level_access = true
  labels                      = local.labels

  lifecycle_rule {
    condition { age = 90 }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }
}

resource "google_bigquery_dataset" "layers" {
  for_each   = toset(["bronze", "silver", "gold", "ops"])
  dataset_id = each.key
  location   = var.bq_location
  labels     = local.labels
}

resource "google_pubsub_topic" "eventos" {
  name   = "alfabetizacao-eventos"
  labels = local.labels
}

resource "google_pubsub_topic" "dlq" {
  name   = "alfabetizacao-eventos-dlq"
  labels = local.labels
}

resource "google_pubsub_subscription" "eventos" {
  name                       = "alfabetizacao-eventos-sub"
  topic                      = google_pubsub_topic.eventos.id
  ack_deadline_seconds       = 60
  message_retention_duration = "604800s"
  labels                     = local.labels

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dlq.id
    max_delivery_attempts = 5
  }
}

# TODO tabelas ops.pipeline_runs e ops.dq_results
# TODO log-based metric + alert policy de falha
# TODO budget alert (precisa do billing account)
# TODO Cloud Run Job + Workflows + Scheduler
