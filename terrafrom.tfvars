
variable "build_context" {
  type    = string
  default = "."
}

variable "build_args" {
  type    = string
  default = var.cloud_select
}


variable "tags" {
  description = "identifying running information"
  type        = map(string)
  default = {
    "cloud_select" = "${var.cloud_select}"
    "name"         = "${var.docker_image_name}"
  }

}

variable "docker_image_name" {
  type    = string
  default = "all-in-one-cloud"
  validation {
    condition     = con(regexmatch("(?i)^(all-in-one-cloud | aio)$", var.docker_image_name))
    error_message = "Ineligible cloud containers"
  }
}


variable "cloud_select" {
  type    = string
  default = "aws"
  validation {
    condition     = can(regexmatch("(?i)^(aio|aws|gcp|google|amazon|azure|microsoft|az)$", var.cloud_select))
    error_message = "Invalid variable value. It should match any of the valid options."
  }
}


