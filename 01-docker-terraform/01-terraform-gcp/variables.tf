variable "credentials" {
  default     = "./.keys/my-creds.json"
  description = "Location of service account credential file"
}

variable "project" {
  default     = "grand-incentive-415912"
  description = "Google Cloud Project ID"
}

variable "location" {
  default     = "EU"
  description = "Location for the project's cloud resources"
}

variable "region" {
  default     = "europe-west1-b"
  description = "Region for the project's cloud resources"
}

variable "gcs_bucket" {
  default     = "grand-incentive-415912-ny-taxi-trips"
  description = "Name for the GCS bucket"
}

variable "storage_class" {
  default     = "STANDARD"
  description = "Storage class for the GCS bucket"
}

variable "bigquery_dataset" {
  default     = "trips_data_all"
  description = "name for the Big Query dataset"
}