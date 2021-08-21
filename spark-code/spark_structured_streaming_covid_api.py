import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as f


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOOTSTRAP_SERVER = "kafka:9092"
TOPIC_NAME = "DEBEZIUM.public.covid_api"

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
    # stream_df.repartition(1).write.options(header='True', delimiter=',').mode('append').csv(os.path.join(project_dir, "output/log_covid_api"))
    
    stream_df.write.mode("append").jdbc(conn, table="public.covid_api", properties=properties)
    stream_df.show(truncate=False)

df \
    .withColumn("value", f.col("value").cast("STRING")) \
    .withColumn("before", f.get_json_object(f.col("value"), "$.before")) \
    .withColumn("after", f.get_json_object(f.col("value"), "$.after")) \
    .withColumn("operation", f.get_json_object(f.col("value"), "$.op")) \
    .withColumn("id_before", f.get_json_object(f.col("before"), "$.id")) \
    .withColumn("id_updated", f.get_json_object(f.col("after"), "$.id")) \
    .withColumn("date_before", f.get_json_object(f.col("before"), "$.date")) \
    .withColumn("date_updated", f.get_json_object(f.col("after"), "$.date")) \
    .withColumn("positive_before", f.get_json_object(f.col("before"), "$.positive")) \
    .withColumn("positive_updated", f.get_json_object(f.col("after"), "$.positive")) \
    .withColumn("death_before", f.get_json_object(f.col("before"), "$.death")) \
    .withColumn("death_updated", f.get_json_object(f.col("after"), "$.death")) \
    .withColumn("recovery_before", f.get_json_object(f.col("before"), "$.recovery")) \
    .withColumn("recovery_updated", f.get_json_object(f.col("after"), "$.recovery")) \
    .withColumn("recover_before", f.get_json_object(f.col("before"), "$.recover")) \
    .withColumn("recover_updated", f.get_json_object(f.col("after"), "$.recover")) \
    .withColumn("scraping_id_before", f.get_json_object(f.col("before"), "$.scraping_id")) \
    .withColumn("scraping_id_updated", f.get_json_object(f.col("after"), "$.scraping_id")) \
    .select("id_before", "id_updated", "date_before", "date_updated", "positive_before", "positive_updated", "death_before", "death_updated",
            "recovery_before", "recovery_updated", "recover_before", "recover_updated", "scraping_id_before", "scraping_id_updated", "operation") \
    .writeStream \
    .foreachBatch(write_postgres) \
    .start() \
    .awaitTermination()