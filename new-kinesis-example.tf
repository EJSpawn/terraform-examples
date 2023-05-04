resource "aws_kinesis_firehose_delivery_stream" "json_delivery_stream" {
  name        = "my-json-delivery-stream"
  destination = "glue"

  s3_configuration {
    role_arn            = "arn:aws:iam::123456789012:role/s3-role"
    bucket_arn          = "arn:aws:s3:::my-bucket"
    buffer_size         = 128
    buffer_interval     = 300
    compression_format  = "GZIP"
    error_output_prefix = "error/"
  }

  extended_s3_configuration {
    role_arn         = "arn:aws:iam::123456789012:role/s3-role"
    bucket_arn       = "arn:aws:s3:::my-bucket"
    prefix           = "sns-events/"
    error_output_prefix = "error/"
    data_format_conversion_configuration {
      schema_configuration {
        database_name = "my_database"
        table_name    = "my_table"
        role_arn      = aws_iam_role.example.arn
      }
      input_format_configuration {
        deserializer {
          open_x_json_ser_de {
            convert_dots_in_json_keys_to_underscores = true
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


data_format_conversion_configuration {
      input_format_configuration {
        deserializer {
          open_x_json_ser_de {
            convert_dots_in_json_keys_to_underscores = true
            field_paths                               = ["$.Message"]
          }
        }
      }
}