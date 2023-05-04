resource "aws_cloudwatch_event_rule" "every_three_hours_lambda_trigger" {
  name                = "every_three_hours_lambda_trigger"
  description         = "Trigger the Lambda function every 3 hours starting at 8 AM"
  schedule_expression = "cron(0 8/3 * * ? *)"
}

resource "aws_cloudwatch_event_target" "invoke_lambda_every_three_hours" {
  rule      = aws_cloudwatch_event_rule.every_three_hours_lambda_trigger.name
  target_id = "InvokeLambdaEveryThreeHours"
  arn       = aws_lambda_function.reparar_particoes_lambda.arn
}

resource "aws_lambda_permission" "allow_event_rule_every_three_hours" {
  statement_id  = "AllowExecutionFromEventBridgeEveryThreeHours"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.reparar_particoes_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_three_hours_lambda_trigger.arn
}