import com.amazonaws.services.glue.AWSGlue;
import com.amazonaws.services.glue.AWSGlueClientBuilder;
import com.amazonaws.services.glue.model.*;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;

import java.util.HashMap;
import java.util.Map;

public class GlueInsertExample {

   public static void main(String[] args) {

      // Set up the Glue and S3 clients
      AWSGlue glue = AWSGlueClientBuilder.defaultClient();
      AmazonS3 s3 = AmazonS3ClientBuilder.defaultClient();

      // Set up the parameters for the insert statement
      String databaseName = "my_database";
      String tableName = "my_table";
      int partitionValue = 20230101;
      String s3Path = "s3://my_bucket/my_path";

      // Create the partition object
      Map<String, String> partitionValues = new HashMap<>();
      partitionValues.put("date", Integer.toString(partitionValue));
      PartitionInput partitionInput = new PartitionInput()
         .withValues(partitionValues)
         .withStorageDescriptor(new StorageDescriptor()
            .withLocation(s3Path)
            .withInputFormat("org.apache.hadoop.mapred.TextInputFormat")
            .withOutputFormat("org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat")
            .withSerdeInfo(new SerDeInfo()
               .withSerializationLibrary("org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe")
               .withParameters(
                  ImmutableMap.of(
                     "serialization.format", "1"
                  )
               )
            )
         );

      // Create the data object
      MyDataObject dataObject = new MyDataObject("hello", "world");

      // Convert the data object to a string
      String dataString = dataObject.toString();

      // Upload the data to S3
      s3.putObject("my_bucket", "my_path/date=" + partitionValue + "/data.parquet", dataString);

      // Create the insert request
      BatchCreatePartitionRequest request = new BatchCreatePartitionRequest()
         .withDatabaseName(databaseName)
         .withTableName(tableName)
         .withPartitionInputList(partitionInput);

      // Execute the insert request
      BatchCreatePartitionResult result = glue.batchCreatePartition(request);
   }

   private static class MyDataObject {
      private String field1;
      private String field2;

      public MyDataObject(String field1, String field2) {
         this.field1 = field1;
         this.field2 = field2;
      }

      public String getField1() {
         return field1;
      }

      public void setField1(String field1) {
         this.field1 = field1;
      }

      public String getField2() {
         return field2;
      }

      public void setField2(String field2) {
         this.field2 = field2;
      }

      @Override
      public String toString() {
         return field1 + "," + field2;
      }
   }
}