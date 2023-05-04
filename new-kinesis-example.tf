resource "aws_kinesis_firehose_delivery_stream" "json_delivery_stream" {
  name        = "my-json-delivery-stream"
  destination = "s3"
  s3_configuration {
    role_arn            = "arn:aws:iam::123456789012:role/s3-role"
    bucket_arn          = "arn:aws:s3:::my-bucket"
    prefix              = "sns-events/"
    buffer_size         = 128
    buffer_interval     = 300
    compression_format  = "GZIP"
    error_output_prefix = "error/"
    data_format_conversion_configuration {
      input_format_configuration {
        deserializer {
          open_x_json_ser_de {
            convert_dots_in_json_keys_to_underscores = true
          }
        }
        schema_configuration {
          database_name = "my_database"
          table_name    = "my_table"
          region        = "us-east-1"
          version_id    = "LATEST"
          role_arn      = "arn:aws:iam::123456789012:role/glue-role"
        }
        input_column_configuration {
          column_name = "message"
          mapping_parameters {
            json_path = "$.Message"
          }
        }
      }
      output_format_configuration {
        serializer {
          open_x_json_ser_de {
            convert_dots_in_json_keys_to_underscores = true
          }
        }
      }
    }
  }
}