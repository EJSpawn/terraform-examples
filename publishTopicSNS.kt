import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.encodeToString
import software.amazon.awssdk.regions.Region
import software.amazon.awssdk.services.sns.SnsClient
import software.amazon.awssdk.services.sns.model.PublishRequest
import software.amazon.awssdk.services.sns.model.MessageAttributeValue
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

@Serializable
data class Pessoa(
    val id: Int,
    val nome: String,
    val idade: Int,
    @SerialName("email_pessoa")
    val email: String,
    val dataCriacao: Int
)

// implementation("software.amazon.awssdk:sns:2.17.66")
// plugins {
//    kotlin("jvm") version "1.6.0"
//    kotlin("plugin.serialization") version "1.6.0"
// } 
//
//implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.3.0")
//
fun main() {
    val dataAtual = LocalDateTime.now()
    val dataCriacao = dataAtual.format(DateTimeFormatter.ofPattern("yyyyMMdd")).toInt()
    val dataParticao = dataAtual.format(DateTimeFormatter.ofPattern("yyyyMMddHHmmss")).toInt()

    val pessoa = Pessoa(1, "João", 25, "joao@email.com", dataCriacao)

    val message = Json.encodeToString(pessoa)

    // Configurar o cliente SNS
    val snsClient = SnsClient.builder()
        .region(Region.US_EAST_1)
        .build()

    // Substitua com o ARN do seu tópico SNS
    val snsTopicArn = "arn:aws:sns:us-east-1:123456789012:meu-topico"

    // Criar atributos de mensagem
    val partitionKey = MessageAttributeValue.builder()
        .dataType("String")
        .stringValue("pessoa_${dataParticao}")
        .build()

    val request = PublishRequest {
        topicArn = topicArn
        message = message
    }

    snsClient.publish(request) // Publica a mensagem no tópico
}