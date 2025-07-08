from pyspark.sql import SparkSession
import pyspark.sql.functions as fc

spark = SparkSession.builder.appName("HW5-Q2-DataFrame").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# TODO: Load film.csv as DataFrame
# TODO: Load actor.csv as DataFrame
# TODO: Load film_actor.csv as DataFrame
film = spark.read.csv("film.csv", header=True, inferSchema=True)
film.createOrReplaceTempView('film')

actor = spark.read.csv("actor.csv", header=True, inferSchema=True)
actor.createOrReplaceTempView('actor')

film_actor = spark.read.csv("film_actor.csv", header=True, inferSchema=True)
film_actor.createOrReplaceTempView('film_actor')

# Q1 TODO - Write DataFrame query
# Replace None with your code
result1 = film.where((film.description.contains('Amazing')) & (film.rental_rate < 1)) \
    .select('title').orderBy('title', ascending=False).limit(5)

result1.show()

# Q1 Output Example:
# +------------------+
# |             title|
# +------------------+
# |      Title1      |
# |      Title2      |
# |      Title3      |
# |      Title4      |
# |      Title5      |
# +------------------+

# %query_1 output:
# +------------------+
# |             title|
# +------------------+
# |       VOICE PEACH|
# |UNBREAKABLE KARATE|
# |         TAXI KICK|
# |       SONG HEDWIG|
# |        SLUMS DUCK|
# +------------------+

# Q2 TODO - Write DataFrame query
# Replace None with your code
result2 = film.where((film.rental_duration >= 3)).groupBy('rating') \
    .agg(fc.avg('rental_rate').alias('avg_rate'), fc.count('*').alias('cnt')) \
    .filter('cnt > 200').select('rating', 'avg_rate')

result2.show()

# Q2 Output Example:
# +------+------------------+
# |rating|          avg_rate|
# +------+------------------+
# |  PG  |     some_value   |
# |PG-13 |     some_value   |
# +------+------------------+

# %query_2 output:
# +------+------------------+
# |rating|          avg_rate|
# +------+------------------+
# | NC-17| 2.970952380952388|
# | PG-13|3.0348430493273613|
# +------+------------------+

# Q3 TODO - Write DataFrame query
# Replace None with your code
t = film_actor.groupBy('actor_id').agg(fc.count('*').alias('cnt'))
max_cnt = t.agg(fc.max('cnt')).collect()[0][0]

result3 = t.filter(t.cnt == max_cnt).select('actor_id')
result3.show()

# Q3 Output Example:
# +--------+
# |actor_id|
# +--------+
# |   ID1  |
# |   ID2  |
# +--------+

# %query_3 output:
# +--------+
# |actor_id|
# +--------+
# |     107|
# +--------+

# Q4 TODO - Write DataFrame query
# Replace None with your code
join_table1 = film_actor.join(actor, film_actor.actor_id == actor.actor_id)
join_table2 = film.join(join_table1, film.film_id == join_table1.film_id)
result4 = join_table2.filter((join_table2.first_name == "TOM") & (join_table2.last_name == "MCKELLEN")) \
    .orderBy('title').select('title').limit(5)
result4.show()

# Q4 Output Example:
# +------------------+
# |             title|
# +------------------+
# |      Title1      |
# |      Title2      |
# |      Title3      |
# |      Title4      |
# |      Title5      |
# +------------------+

# %query_4 output:
# +------------------+
# |             title|
# +------------------+
# |  ANALYZE HOOSIERS|
# |   CADDYSHACK JEDI|
# |     CLUB GRAFFITI|
# |CONGENIALITY QUEST|
# |      DESIRE ALIEN|
# +------------------+


# Q5 TODO - Write DataFrame query
# Replace None with your code
condition1 = [row[0] for row in film_actor.filter('film_id = 23').select('actor_id').collect()]
condition2 = [row[0] for row in film_actor.filter('film_id = 1').select('actor_id').collect()]

result5 = actor.where((actor.actor_id.isin(condition1)) & (~actor.actor_id.isin(condition2))) \
    .orderBy('first_name').select('first_name', 'last_name')
result5.show()

# Q5 Output Example:
# +----------+---------+
# |first_name|last_name|
# +----------+---------+
# |   Name1  | Surname1|
# |   Name2  | Surname2|
# |   Name3  | Surname3|
# +----------+---------+

# %query_5 output:
# +----------+---------+
# |first_name|last_name|
# +----------+---------+
# |     ELVIS|     MARX|
# |  HUMPHREY|   WILLIS|
# |     JAYNE|    NOLTE|
# |  JENNIFER|    DAVIS|
# +----------+---------+
