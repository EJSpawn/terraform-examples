
import java.util.List;

public class EventDTO {
    private IntegrationType integrationType;
    private ProcessingType processingType;
    private List<String> dateRange;
    private List<String> specificDates;

    // Getters, setters e possivelmente construtores e métodos úteis...
}

<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.x.x</version> <!-- Use a versão mais recente -->
</dependency>

package example;

import software.amazon.awssdk.services.lambda.runtime.Context;
import software.amazon.awssdk.services.lambda.runtime.RequestHandler;
import com.fasterxml.jackson.databind.ObjectMapper;

public class EventBridgeHandler implements RequestHandler<String, String> {

    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    @Override
    public String handleRequest(String input, Context context) {
        try {
            EventDTO event = OBJECT_MAPPER.readValue(input, EventDTO.class);
            
            context.getLogger().log("Received Event: " + event);

            // Processamento adicional...

            return "Event processed successfully!";
        } catch (Exception e) {
            context.getLogger().log("Error processing event: " + e.getMessage());
            return "Error processing event.";
        }
    }
}