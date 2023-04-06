provider "aws" {
  region     = "us-east-1"
}

# Criar o tópico SNS
resource "aws_sns_topic" "example_topic" {
  name = "example_topic"
}

# Criar a política de assinatura para permitir o envio para o Firehose
resource "aws_iam_policy" "firehose_policy" {
  name = "firehose_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "firehose:PutRecord",
          "firehose:PutRecordBatch"
        ]
        Resource = aws_kinesis_firehose_delivery_stream.example_stream.arn
      }
    ]
  })
}

# Criar a assinatura do tipo Kinesis Data Firehose Delivery Stream
resource "aws_sns_topic_subscription" "example_subscription" {
  topic_arn = aws_sns_topic.example_topic.arn
  protocol  = "firehose"
  endpoint  = aws_kinesis_firehose_delivery_stream.example_stream.arn

  # Anexar a política de assinatura para permitir o envio para o Firehose
  depends_on = [aws_iam_policy.firehose_policy]
}

# Criar a tabela do Hive no AWS Glue Catalog
resource "aws_glue_catalog_table" "example_table" {
  name = "example_table"
  database_name = "example_database"
  table_type = "EXTERNAL_TABLE"
  parameters = {
    "classification" = "json"
    "compressionType" = "gzip"
    "typeOfData" = "file"
    "update_date_format" = "yyyy-MM-dd HH:mm:ss"
    "update_date_key" = "update_date"
  }
  partition_keys = [
    {
      name = "dt"
      type = "date"
    }
  ]
  storage_descriptor {
    location = "s3://example-bucket/example-data/"
    input_format = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
    ser_de_info {
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
    }
    columns {
      name = "column1"
      type = "string"
    }
    columns {
      name = "column2"
      type = "int"
    }
  }
}

resource "aws_kinesis_firehose_delivery_stream" "example_stream" {
  name        = "example_stream"
  destination = "glue"

  glue_configuration {
    database_name = aws_glue_catalog_table.example_table.database_name
    table_name    = aws_glue_catalog_table.example_table.name

    partition_configuration {
      # Utilizar a coluna "dt" como chave de partição
      partition_columns = ["dt"]
    }
  }

  s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.example_bucket.arn
    prefix     = "data/"
    buffer_size = 5
    buffer_interval = 300
  }
}