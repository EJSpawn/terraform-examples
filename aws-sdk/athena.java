import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.athena.AthenaClient;
import software.amazon.awssdk.services.athena.model.*;

import java.util.List;

public class AthenaExample {
    public static void main(String[] args) {
        // Criação do cliente
        AthenaClient athenaClient = AthenaClient.builder()
            .region(Region.US_EAST_1)  // substitua pela sua região
            .build();

        // Definição da consulta
        String query = "SELECT * FROM my_database.my_table";

        // Configuração da consulta
        QueryExecutionContext queryContext = QueryExecutionContext.builder()
            .database("my_database")  // substitua pelo seu banco de dados
            .build();

        ResultConfiguration resultConfig = ResultConfiguration.builder()
            .outputLocation("s3://my-output-bucket/path/")  // substitua pelo seu bucket
            .build();

        // Execução da consulta
        StartQueryExecutionRequest startQueryRequest = StartQueryExecutionRequest.builder()
            .queryString(query)
            .queryExecutionContext(queryContext)
            .resultConfiguration(resultConfig)
            .build();

        StartQueryExecutionResponse startQueryResponse = athenaClient.startQueryExecution(startQueryRequest);
        String queryExecutionId = startQueryResponse.queryExecutionId();

        // Obtenção dos resultados
        GetQueryExecutionRequest getQueryExecutionRequest = GetQueryExecutionRequest.builder()
            .queryExecutionId(queryExecutionId)
            .build();

        GetQueryExecutionResponse getQueryExecutionResponse;
        boolean isQueryStillRunning = true;

        // Aguarda a conclusão da consulta
        do {
            getQueryExecutionResponse = athenaClient.getQueryExecution(getQueryExecutionRequest);
            String queryState = getQueryExecutionResponse.queryExecution().status().state().toString();
            if (queryState.equals(QueryExecutionState.FAILED.toString())) {
                throw new RuntimeException("A consulta falhou ao executar.");
            } else if (queryState.equals(QueryExecutionState.CANCELLED.toString())) {
                throw new RuntimeException("A consulta foi cancelada.");
            } else if (queryState.equals(QueryExecutionState.SUCCEEDED.toString())) {
                isQueryStillRunning = false;
            } else {
                // A consulta ainda está sendo executada. Espere um pouco.
                try {
                    Thread.sleep(1000);  // espera 1 segundo antes de verificar novamente
                } catch (InterruptedException e) {
                    throw new RuntimeException("A thread foi interrompida.", e);
                }
            }
        } while (isQueryStillRunning);

        // A consulta foi concluída. Obtenha os resultados.
        GetQueryResultsRequest getQueryResultsRequest = GetQueryResultsRequest.builder()
            .queryExecutionId(queryExecutionId)
            .build();

        GetQueryResultsResponse getQueryResultsResponse = athenaClient.getQueryResults(getQueryResultsRequest);
        List<Row> results = getQueryResultsResponse.resultSet().rows();
        
        for (Row row : results) {
            List<Datum> data = row.data();
            String id = data.get(0).varCharValue();     // Obter valor de id
            String nome = data.get(1).varCharValue();   // Obter valor de nome
            String idade = data.get(2).varCharValue();  // Obter valor de idade
            System.out.println("ID: " + id + ", Nome: " + nome + ", Idade: " + idade);
        }
    }
}