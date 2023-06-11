terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {}

resource "docker_image" "all-in-one-cloud" {
  name = var.docker_image_name
  build {
    context = var.build_context
    tag = {
      product = var.cloud_select

    }
  }
  triggers = {
    dir_sha1 = sha1(join("", [for f in fileset(path.module, "all-in-one-cloud/*") : filesha1(f)]))
  }
  keep_locally = false
}

resource "docker_container" "AIO" {
  image = var.docker_image_name
  name  = "AIO"
}
