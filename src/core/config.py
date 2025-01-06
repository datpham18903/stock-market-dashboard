from pyspark.sql import SparkSession

def init_spark():
    return (
        SparkSession.builder.appName("Stock Dashboard")
        .config("spark.driver.memory", "4g")
        .config("spark.executor.memory", "4g")
        .config("spark.sql.execution.arrow.enabled", "true")
        .getOrCreate()
    )


