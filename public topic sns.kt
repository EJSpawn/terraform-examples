import aws.sdk.kotlin.services.sns.SnsClient;
import aws.sdk.kotlin.services.sns.model.PublishRequest;

fun main() {
    val snsClient = SnsClient { region = "us-east-1" } // Crie um cliente SNS

    val topicArn = "arn:aws:sns:us-east-1:123456789012:my-topic" // ARN do tópico

    val message = "Hello, world!" // Mensagem a ser publicada

    val request = PublishRequest {
        topicArn = topicArn
        message = message
    }

    snsClient.publish(request) // Publica a mensagem no tópico
}