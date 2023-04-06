provider "aws" {
  region = "us-east-1"
}

resource "aws_sns_topic" "my_topic" {
  name = "my-topic"
}

resource "aws_sns_topic_subscription" "my_topic_subscription" {
  topic_arn = aws_sns_topic.my_topic.arn
  protocol  = "email"
  endpoint  = "user@example.com"
}