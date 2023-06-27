variable "parametro" {
  description = "A list of maps with fields 'data_execucao' and 'periodo_reprocessamento'"
  type = list(object({
    data_execucao           = string
    periodo_reprocessamento = list(string)
  }))
  default = [
    {
      data_execucao = "2023-06-26"
      periodo_reprocessamento = ["2023-06-24", "2023-06-25"]
    },
    {
      data_execucao = "2023-06-27"
      periodo_reprocessamento = ["2023-06-25", "2023-06-26"]
    }
  ]
}

resource "aws_cloudwatch_event_rule" "example" {
  count               = length(var.parametro)
  name                = "example-rule-${count.index}"
  schedule_expression = "cron(0 12 ${element(var.parametro, count.index).data_execucao} * ? *)"
  description         = "Fires every day at noon"
}

resource "aws_cloudwatch_event_target" "example" {
  count = length(var.parametro)
  rule  = aws_cloudwatch_event_rule.example[count.index].name
  arn   = aws_lambda_function.my_lambda_function.arn
  input = jsonencode({
    "periodo_reprocessamento" = element(var.parametro, count.index).periodo_reprocessamento
  })
}