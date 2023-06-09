from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, lower

spark = SparkSession.builder.getOrCreate()

# Supondo que df seja o seu DataFrame e 'coluna' seja o nome da coluna que deseja converter
df = spark.createDataFrame([
    ("Sim",),
    ("Não",),
    ("",),
    ("-"),
    ("sIM"),
    ("NÃO"),
], ["coluna"])

df = df.withColumn("coluna", 
                   when(lower(col("coluna")) == 'sim', True)
                   .when(lower(col("coluna")) == 'não', False)
                   .otherwise(None))

df.show()