# Definir o provedor AWS
provider "aws" {
  region = "us-east-1"
}

# Criar uma fila SQS
resource "aws_sqs_queue" "my_queue" {
  name = "my-queue"
}

# Criar uma fila de destino morto (DLQ)
resource "aws_sqs_queue" "my_queue_dlq" {
  name = "my-queue-dlq"
}

# Criar um tópico SNS com uma fila de destino morto (DLQ)
resource "aws_sns_topic" "my_topic" {
  name = "my-topic"
  
  # Configurar a fila de destino morto para receber mensagens que não foram entregues ao destino principal
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.my_queue_dlq.arn
    maxReceiveCount = 3
  })
}

# Criar uma assinatura para o tópico SNS
resource "aws_sns_topic_subscription" "my_topic_subscription" {
  topic_arn = aws_sns_topic.my_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.my_queue.arn
}