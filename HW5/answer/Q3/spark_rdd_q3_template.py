from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("HW5-Q3-RDD").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
sc = spark.sparkContext

# TODO: Load film.csv as RDD
# TODO: Load actor.csv as RDD
# TODO: Load film_actor.csv as RDD
film = spark.read.csv("film.csv", header=True, inferSchema=True)
film.createOrReplaceTempView('film')
film_rdd = film.rdd.repartition(2)

actor = spark.read.csv("actor.csv", header=True, inferSchema=True)
actor.createOrReplaceTempView('actor')
actor_rdd = actor.rdd.repartition(2)

film_actor = spark.read.csv("film_actor.csv", header=True, inferSchema=True)
film_actor.createOrReplaceTempView('film_actor')
film_actor_rdd = film_actor.rdd.repartition(2)


# Q1  TODO - Write RDD transformation logic
# Replace None with your code
result1 = film_rdd.filter(lambda r: ('Amazing' in  r['description']) & (r['rental_rate'] < 1)) \
    .map(lambda r: r['title']).sortBy(lambda r: r, ascending = False).take(5)
print(result1)

# Q1 Output Example:
# ['Title1', 'Title2', 'Title3', 'Title4', 'Title5']

# %query_1 output:
# ['VOICE PEACH', 'UNBREAKABLE KARATE', 'TAXI KICK', 'SONG HEDWIG', 'SLUMS DUCK']

# Q2  TODO - Write RDD transformation logic
# Replace None with your code
result2 = film_rdd.filter(lambda r: r['rental_duration'] >= 3) \
    .map(lambda r: (r['rating'], (r['rental_rate'], 1))) \
    .reduceByKey(lambda U, v: (U[0]+v[0], U[1]+v[1])) \
    .filter(lambda kv: kv[1][1] > 200) \
    .mapValues(lambda r: r[0]/r[1]).collect()
print(result2)

# Q2 Output Example:
# [('PG', avg_value), ('PG-13', avg_value)]

# %query_2 output:
# [('NC-17', 2.9709523809523857), ('PG-13', 3.0348430493273595)]

# Q3  TODO - Write RDD transformation logic
# Replace None with your code
t = film_actor_rdd.map(lambda r: (r['actor_id'], 1)).reduceByKey(lambda U, x: U+x)
max_cnt = t.max(key = lambda x: x[1])[1]
result3 = t.filter(lambda r: r[1] == max_cnt).map(lambda r: (r[0], )).collect()
print(result3)

# Q3 Output Example:
# [(actor_id1,), (actor_id2,)]

# %query_3 output:
# [(107,)]

# Q4  TODO - Write RDD transformation logic
# Replace None with your code
_film_rdd = film_rdd.map(lambda r: (r['film_id'], r['title']))
_film_actor_rdd = film_actor_rdd.map(lambda r: (r['film_id'], r['actor_id']))
_join = _film_actor_rdd.join(_film_rdd)
_join1 = _join.map(lambda kv: (kv[1][0], kv[1][1]))
_actor_rdd = actor_rdd.map(lambda r: (r['actor_id'], (r['first_name'], r['last_name'])))
result4 = _actor_rdd.join(_join1) \
    .filter(lambda r: (r[1][0][0] == "TOM") & (r[1][0][1] == "MCKELLEN")) \
    .map(lambda r: r[1][1]) \
    .sortBy(lambda r: r).take(5) 

print(result4)

# Q4 Output Example:
# ['Title1', 'Title2', 'Title3', 'Title4', 'Title5']


# %query_4 output:
# ['ANALYZE HOOSIERS', 'CADDYSHACK JEDI', 'CLUB GRAFFITI', 'CONGENIALITY QUEST', 'DESIRE ALIEN']

# Q5  TODO - Write RDD transformation logic
# Replace None with your code
condition1 = film_actor_rdd.filter(lambda r: r['film_id'] == 23).map(lambda x: x['actor_id']).collect()
condition2 = film_actor_rdd.filter(lambda r: r['film_id'] == 1).map(lambda x: x['actor_id']).collect()
result5 = actor_rdd.filter(lambda r: (r['actor_id'] in condition1) & (r['actor_id'] not in condition2)) \
    .map(lambda r: (r['first_name'], r['last_name'])) \
    .sortBy(lambda x: x[0]).collect()
print(result5)

# Q5 Output Example:
# [('FirstName1', 'LastName1'), ('FirstName2', 'LastName2'), ('FirstName3', 'LastName3')]

# %query_5 output:
# [('ELVIS', 'MARX'), ('HUMPHREY', 'WILLIS'), ('JAYNE', 'NOLTE'), ('JENNIFER', 'DAVIS')]