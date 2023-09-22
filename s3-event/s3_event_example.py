s3_event = {
    "Records": [
        {
            "eventVersion": "2.1",
            "eventSource": "aws:s3",
            "awsRegion": "us-west-2",
            "eventTime": "2021-09-21T20:00:00Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {
                "principalId": "EXAMPLE"
            },
            "requestParameters": {
                "sourceIPAddress": "ip-address"
            },
            "responseElements": {
                "x-amz-request-id": "request-id",
                "x-amz-id-2": "host-id"
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "config-id",
                "bucket": {
                    "name": "bucket-name",
                    "ownerIdentity": {
                        "principalId": "EXAMPLE"
                    },
                    "arn": "bucket-ARN"
                },
                "object": {
                    "key": "object-key",
                    "size": 1234,
                    "eTag": "eTag",
                    "versionId": "version-id",
                    "sequencer": "sequence-id"
                }
            }
        }
    ]
}

object_key = s3_event["Records"][0]["s3"]["object"]["key"]