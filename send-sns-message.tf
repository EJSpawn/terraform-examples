provider "aws" {
  region = "us-east-1"
}

locals {
  message = "Hello, SNS!" # Mensagem que será enviada para o tópico SNS
}

data "aws_sns_topic" "example_topic" {
  arn = "arn:aws:sns:us-east-1:123456789012:example_topic" # Coloque aqui o ARN do tópico SNS existente
}

resource "null_resource" "sns_publish" {
  triggers = {
    message = local.message
  }

  provisioner "local-exec" {
    command = <<-EOT
      aws sns publish --topic-arn "${data.aws_sns_topic.example_topic.arn}" --message "${local.message}"
    EOT
  }
}