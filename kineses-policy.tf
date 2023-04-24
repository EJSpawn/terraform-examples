resource "aws_iam_policy" "kinesis_firehose_s3_policy" {
  name        = "kinesis_firehose_s3_policy"
  description = "Policy for Kinesis Firehose to write data to S3"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "AllowKinesisFirehoseDeliveryStreamManagement"
        Effect   = "Allow"
        Action   = [
          "firehose:CreateDeliveryStream",
          "firehose:DeleteDeliveryStream",
          "firehose:DescribeDeliveryStream",
          "firehose:ListDeliveryStreams",
          "firehose:StartDeliveryStreamEncryption",
          "firehose:StopDeliveryStreamEncryption",
          "firehose:TagDeliveryStream",
          "firehose:UntagDeliveryStream",
          "firehose:UpdateDestination",
          "firehose:UpdateDestinationVersion",
          "firehose:PutRecordBatch",
          "firehose:PutRecord",
          "firehose:TagDeliveryStream",
          "firehose:UntagDeliveryStream"
        ]
        Resource = "arn:aws:firehose:*:*:deliverystream/*"
      },
      {
        Sid      = "AllowS3ReadWriteAccess"
        Effect   = "Allow"
        Action   = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket",
          "s3:GetBucketLocation",
          "s3:GetObjectVersion",
          "s3:GetBucketPolicy",
          "s3:PutBucketPolicy",
          "s3:DeleteObject"
        ]
        Resource = [
          "arn:aws:s3:::my-bucket",
          "arn:aws:s3:::my-bucket/*"
        ]
      },
      {
        Sid      = "AllowSNSTopicPublish"
        Effect   = "Allow"
        Action   = [
          "sns:Publish"
        ]
        Resource = "arn:aws:sns:*:*:my-topic"
      },
      {
        Sid      = "AllowKMSKeyManagement"
        Effect   = "Allow"
        Action   = [
          "kms:CreateGrant",
          "kms:Decrypt",
          "kms:DescribeKey",
          "kms:GenerateDataKey",
          "kms:GenerateDataKeyWithoutPlaintext",
          "kms:ReEncryptFrom",
          "kms:ReEncryptTo",
          "kms:RevokeGrant",
          "kms:TagResource",
          "kms:UntagResource",
          "kms:UpdateAlias",
          "kms:UpdateKeyDescription"
        ]
        Resource = "arn:aws:kms:*:*:key/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "kinesis_firehose_s3_policy_attachment" {
  policy_arn = aws_iam_policy.kinesis_firehose_s3_policy.arn
  role       = aws_iam_role.my_role.name
}
