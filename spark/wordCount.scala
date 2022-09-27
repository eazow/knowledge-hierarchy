import org.apache.spark.rdd.RDD
 
val rootPath: String = "/Users/01398068/spark/spark-3.1.2-bin-hadoop3.2/tests"
val file: String = s"${rootPath}/spark.txt"
 
// 读取文件内容
val lineRDD: RDD[String] = spark.sparkContext.textFile(file) 

// 以行为单位做分词
val wordRDD: RDD[String] = lineRDD.flatMap(line => line.split(" "))
val cleanWordRDD: RDD[String] = wordRDD.filter(word => !word.equals(""))
 
// 把RDD元素转换为（Key，Value）的形式
val kvRDD: RDD[(String, Int)] = cleanWordRDD.map(word => (word, 1))
// 按照单词做分组计数
val wordCounts: RDD[(String, Int)] = kvRDD.reduceByKey((x, y) => x + y)
 
// 打印词频最高的5个词汇
wordCounts.map{case (k, v) => (v, k)}.sortByKey(false).take(5)
