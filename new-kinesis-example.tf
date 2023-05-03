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