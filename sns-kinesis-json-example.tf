# Cria um stream no Kinesis Firehose
resource "aws_kinesis_firehose_delivery_stream" "example_stream" {
  name        = "example-stream"
  destination = "glue"
  
  # Configura as informações de conexão do Glue
  glue_configuration {
    database_name = "example_database"
    table_name    = "example_table"
  }

  # Configura as opções de formatação de saída
  s3_configuration {
    role_arn           = aws_iam_role.example.arn
    bucket_arn         = aws_s3_bucket.example.arn
    prefix             = "example_prefix/"
    buffer_size        = 64
    buffer_interval    = 400
    compression_format = "UNCOMPRESSED"
  }

  # Configura o formato de entrada dos dados como CSV
  extended_s3_configuration {
    processing_configuration {
      enabled = false
    }
    csv {
      delimiter = ","
      quote_escape = "\""
    }
  }
}

# Cria uma tabela no AWS Glue
resource "aws_glue_table" "example_table" {
  name     = "example_table"
  database = "example_database"

  table_input {
    description = "Example table"
    name        = "example_table"
    parameters = {
      "classification" = "csv"
      "compressionType" = "none"
      "delimiter" = ","
      "header" = "true"
    }

    storage_descriptor {
      input_format        = "org.apache.hadoop.mapred.TextInputFormat"
      output_format       = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
      location            = "s3://${aws_s3_bucket.example.bucket}/example_table/"
      compressed          = false
      serde_info {
        name                  = "example_table"
        serde_library         = "org.apache.hadoop.hive.serde2.OpenCSVSerde"
        serde_parameters = {
          "escapeChar" = "\\"
          "quoteChar"  = "\""
          "separatorChar" = ","
        }
      }
    }
  }
}