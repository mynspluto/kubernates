from pyspark.sql import SparkSession

if __name__ == "__main__":
    # SparkSession 생성
    spark = SparkSession.builder \
        .appName("Example Spark Script") \
        .getOrCreate()

    # 예제 데이터 프레임 생성
    data = [("Alice", 34), ("Bob", 45), ("Charlie", 28)]
    df = spark.createDataFrame(data, ["Name", "Age"])

    # 데이터 출력
    df.show()

    # SparkSession 종료
    spark.stop()

#spark-submit --master local hello.py