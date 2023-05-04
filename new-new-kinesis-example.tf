resource "aws_kinesis_firehose_delivery_stream" "my_kinesis_fh" {
  for_each    = var.my_bucket_map
  name        = "${lower(each.value.name)}.${lower(each.value.suffix)}"
  destination = "extended_s3"

  extended_s3_configuration {
    role_arn        = aws_iam_role.my_firehose_role.arn
    bucket_arn      = aws_s3_bucket.my_bucket[each.key].arn
    buffer_size     = 128
    buffer_interval = 60

    data_format_conversion_configuration {
      input_format_configuration {
        deserializer {
          open_x_json_ser_de {
          }
        }
      }

      output_format_configuration {
        serializer {
          parquet_ser_de {
          }
        }
      }

      schema_configuration {
        database_name = aws_glue_catalog_database.my_glue_db.name
        role_arn      = aws_iam_role.my_firehose_role.arn
        table_name    = aws_glue_catalog_table.my_glue[each.key].name
      }
    }
  }

}