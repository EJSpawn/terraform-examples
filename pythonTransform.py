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




from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, from_unixtime

def converter_colunas_para_timestamp(df, colunas):
    for coluna in colunas:
        try:
            df = df.withColumn(coluna, from_unixtime(unix_timestamp(col(coluna), "dd/MM/yyyy HH:mm:ss")))
        except:
            df = df.withColumn(coluna, None)
    return df

# Crie uma sessão Spark
spark = SparkSession.builder.getOrCreate()

# Crie um DataFrame de exemplo
data = [("15/09/2021 10:30:00", "16/09/2021 15:45:00", "17/09/2021 08:00:00", "2021-09-18")]
df = spark.createDataFrame(data, ["coluna1", "coluna2", "coluna3", "coluna4"])

# Colunas para converter
colunas_para_converter = ["coluna1", "coluna2", "coluna3", "coluna4"]

# Chame a função para converter as colunas para o formato de timestamp
df_convertido = converter_colunas_para_timestamp(df, colunas_para_converter)

# Exiba o DataFrame resultante
df_convertido.show()