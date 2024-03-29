data "ec_deployment" "logging" {
  id = local.logging_cluster_id
}

data "ec_stack" "latest" {
  version_regex = "latest"
  region        = "us-east-1"
}


resource "ec_deployment" "knowledge-graph" {
  name                   = "knowledge-graph"
  region                 = "eu-west-1"
  version                = data.ec_stack.latest.version
  deployment_template_id = "aws-io-optimized-v2"

  elasticsearch {
    topology {
      id         = "hot_content"
      size       = "1g"
      zone_count = 2
    }
  }

  # The catalogue-api cluster gets the pipeline-storage clusters added
  # as remote clusters dynamically.  We don't want these to be rolled
  # back when we change the Terraform, so ignore any changes here.
  lifecycle {
    ignore_changes = [elasticsearch[0].remote_cluster]
  }

  observability {
    deployment_id = data.ec_deployment.logging.id
  }

  kibana {
    topology {
      size       = "1g"
      zone_count = 1
    }
  }
}
