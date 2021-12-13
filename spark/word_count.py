from pyspark import SparkContext

text = SparkContext.getOrCreate().textFile("./data/spark.txt")
top5_words = (
    text.flatMap(lambda line: line.split(" "))
    .filter(lambda word: word != "")
    .map(lambda word: (word, 1))
    .reduceByKey(lambda x, y: x + y)
    .sortBy(lambda x: x[1], False)
    .take(5)
)
print(top5_words)
