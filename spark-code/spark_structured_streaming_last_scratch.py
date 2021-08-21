import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as f


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOOTSTRAP_SERVER = "kafka:9092"
TOPIC_NAME = "DEBEZIUM.public.last_scratch"

spark = SparkSession \
    .builder \
    .config('spark.driver.extraClassPath', os.path.join(project_dir, 'connector/postgresql-9.4.1207.jar')) \
    .appName("Structured Streaming Update Data Apps") \
    .getOrCreate()
    
spark.sparkContext.setLogLevel('WARN')

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVER) \
    .option("subscribe", TOPIC_NAME) \
    .option("startingOffsets", "earliest") \
    .load()


# String connection to postgres-dwh
conn: str = "jdbc:postgresql://postgres-dwh:5432/warehouse"
properties: dict = {
    "user": "warehouse",
    "password": "warehouse",
    "driver": "org.postgresql.Driver"
}

def write_postgres(stream_df, stream_id):
    # write to csv
    # stream_df.repartition(1).write.options(header='True', delimiter=',').mode('append').csv(os.path.join(project_dir, "output/log_last_scratch"))
    
    stream_df.write.mode("append").jdbc(conn, table="public.last_scratch", properties=properties)
    stream_df.show(truncate=False)

df \
    .withColumn("value", f.col("value").cast("STRING")) \
    .withColumn("before", f.get_json_object(f.col("value"), "$.before")) \
    .withColumn("after", f.get_json_object(f.col("value"), "$.after")) \
    .withColumn("operation", f.get_json_object(f.col("value"), "$.op")) \
    .withColumn("id_before", f.get_json_object(f.col("before"), "$.id")) \
    .withColumn("id_updated", f.get_json_object(f.col("after"), "$.id")) \
    .withColumn("last_get_before", f.get_json_object(f.col("before"), "$.last_get")) \
    .withColumn("last_get_updated", f.get_json_object(f.col("after"), "$.last_get")) \
    .withColumn("active_before", f.get_json_object(f.col("before"), "$.active")) \
    .withColumn("active_updated", f.get_json_object(f.col("after"), "$.active")) \
    .select("id_before", "id_updated", "last_get_before", "last_get_updated", "active_before", "active_updated","operation") \
    .writeStream \
    .foreachBatch(write_postgres) \
    .start() \
    .awaitTermination()