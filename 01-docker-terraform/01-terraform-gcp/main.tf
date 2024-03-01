terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.18.0"
    }
  }
}

provider "google" {
  # credentials = "./.keys/my-creds.json"
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

# GOOGLE CLOUD STORAGE BUCKET
resource "google_storage_bucket" "gcs_bucket" {
  name          = var.gcs_bucket
  location      = var.location
  force_destroy = true
  storage_class = var.storage_class

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}


# GOOGLE BIGQUERY DATASET
resource "google_bigquery_dataset" "bigquery_dataset" {
  dataset_id    = var.bigquery_dataset
  location      = var.location
  delete_contents_on_destroy = true
}