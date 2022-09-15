import org.apache.spark.rdd.RDD
import org.apache.spark.sql.types.{StringType, IntegerType, StructField, StructType}
import org.apache.spark.sql.Row
import org.apache.spark.sql.DataFrame

val seq: Seq[(String, Int)] = Seq(("Bob", 10), ("Alice", 18))
val rdd: RDD[(String, Int)] = sc.parallelize(seq)

val schema:StructType = StructType(Array(StructField("name", StringType),StructField("age", IntegerType)))

val rowRDD: RDD[Row] = rdd.map(fields => Row(fields._1, fields._2))

val dataFrame: DataFrame = spark.createDataFrame(rowRDD,schema)
dataFrame.show