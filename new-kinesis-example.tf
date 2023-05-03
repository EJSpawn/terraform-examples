provider "aws" {
  region = "us-east-1"
}

resource "aws_sns_topic" "my_topic" {
  name = "my-topic"
}

resource "aws_glue_catalog_database" "my_database" {
  name = "my_database"
}

resource "aws_glue_catalog_table" "my_table" {
  name          = "my_table"
  database_name = aws_glue_catalog_database.my_database.name
  table_type    = "EXTERNAL_TABLE"
  parameters = {
    "classification" = "json"
  }
  
  storage_descriptor {
    location         = "s3://my-bucket/sns-events/"
    input_format     = "org.apache.hadoop.mapred.TextInputFormat"
    output_format    = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
    serde_info {
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
    }
  }
}

resource "aws_kinesis_firehose_delivery_stream" "my_delivery_stream" {
  name        = "my-delivery-stream"
  destination = "glue"
  
  s3_configuration {
    role_arn         = "arn:aws:iam::123456789012:role/firehose-role"
    bucket_arn       = "arn:aws:s3:::my-bucket"
    prefix           = "sns-events/"
    buffer_size      = 128
    buffer_interval  = 900
    compression_type = "GZIP"
  }

  destination_configuration {
    glue_configuration {
      role_arn         = "arn:aws:iam::123456789012:role/glue-role"
      database_name    = aws_glue_catalog_database.my_database.name
      table_name       = aws_glue_catalog_table.my_table.name
      s3_bucket_prefix = "sns-events/"
      buffer_size      = 128
      buffer_interval  = 900
    }
  }
}

resource "aws_sns_topic_subscription" "my_subscription" {
  topic_arn = aws_sns_topic.my_topic.arn
  protocol  = "sqs"
  endpoint  = aws_kinesis_firehose_delivery_stream.my_delivery_stream.sqs_queue_url
}
provider "aws" {
  region = "us-east-1"
}

resource "aws_sns_topic" "my_topic" {
  name = "my-topic"
}

resource "aws_glue_catalog_database" "my_database" {
  name = "my_database"
}

resource "aws_glue_catalog_table" "my_table" {
  name          = "my_table"
  database_name = aws_glue_catalog_database.my_database.name
  table_type    = "EXTERNAL_TABLE"
  parameters = {
    "classification" = "json"
  }
  
  storage_descriptor {
    location         = "s3://my-bucket/sns-events/"
    input_format     = "org.apache.hadoop.mapred.TextInputFormat"
    output_format    = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
    serde_info {
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
    }
  }
}

resource "aws_kinesis_firehose_delivery_stream" "my_delivery_stream" {
  name        = "my-delivery-stream"
  destination = "glue"
  
  s3_configuration {
    role_arn         = "arn:aws:iam::123456789012:role/firehose-role"
    bucket_arn       = "arn:aws:s3:::my-bucket"
    prefix           = "sns-events/"
    buffer_size      = 128
    buffer_interval  = 900
    compression_type = "GZIP"
  }

  destination_configuration {
    glue_configuration {
      role_arn         = "arn:aws:iam::123456789012:role/glue-role"
      database_name    = aws_glue_catalog_database.my_database.name
      table_name       = aws_glue_catalog_table.my_table.name
      s3_bucket_prefix = "sns-events/"
      buffer_size      = 128
      buffer_interval  = 900
    }
  }
}

resource "aws_sns_topic_subscription" "my_subscription" {
  topic_arn = aws_sns_topic.my_topic.arn
  protocol  = "sqs"
  endpoint  = aws_kinesis_firehose_delivery_stream.my_delivery_stream.sqs_queue_url
}
