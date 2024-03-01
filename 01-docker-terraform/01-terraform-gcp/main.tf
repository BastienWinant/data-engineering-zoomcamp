terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.18.0"
    }
  }
}

provider "google" {
  credentials = "./.keys/my-creds.json"
  project     = "grand-incentive-415912"
  region      = "europe-west1-b"
}