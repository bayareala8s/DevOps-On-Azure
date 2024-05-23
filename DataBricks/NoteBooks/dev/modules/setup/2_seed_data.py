# Databricks notebook source
# MAGIC %pip install faker

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, rand
from pyspark.sql.types import StringType, DateType
from faker import Faker
import datetime

# Initialize Faker
fake = Faker()

# Generate 1000 records
data = [(fake.uuid4(), fake.user_name(), fake.password(), fake.email(), fake.date_between(start_date='-1y', end_date='today')) for _ in range(1000)]

# Create DataFrame
df = spark.createDataFrame(data, ["user_id", "username", "password", "email", "created_at"])

# Write to Delta table
df.write.format("delta").mode("append").partitionBy("created_at").save("abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/users")

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, rand
from pyspark.sql.types import StringType, DateType, DecimalType
from faker import Faker
import datetime

# Initialize Faker
fake = Faker()

# Generate 1000 records
data = [(fake.uuid4(), fake.catch_phrase(), fake.text(), fake.uuid4(), fake.pydecimal(left_digits=5, right_digits=2, positive=True), fake.date_between(start_date='-1y', end_date='today')) for _ in range(1000)]

# Create DataFrame
df = spark.createDataFrame(data, ["product_id", "product_name", "product_description", "category_id", "price", "created_at"])

df = df.withColumn("price", df["price"].cast(DecimalType(10, 2)))

# Write to Delta table
df.write.format("delta").mode("append").partitionBy("created_at").save("abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/products")

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, rand
from pyspark.sql.types import StringType
from faker import Faker

# Initialize Faker
fake = Faker()

# Generate 1000 records
data = [(fake.uuid4(), fake.catch_phrase()) for _ in range(1000)]

# Create DataFrame
df = spark.createDataFrame(data, ["category_id", "category_name"])

# Write to Delta table
df.write.format("delta").mode("append").save("abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/product_categories")

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, rand
from pyspark.sql.types import StringType, IntegerType, DateType
from faker import Faker
import datetime

# Initialize Faker
fake = Faker()

# Generate 1000 records
data = [(fake.uuid4(), fake.uuid4(), fake.uuid4(), fake.random_int(min=1, max=10), fake.date_between(start_date='-1y', end_date='today')) for _ in range(1000)]

# Create DataFrame
df = spark.createDataFrame(data, ["cart_id", "user_id", "product_id", "quantity", "added_at"])

df = df.withColumn("quantity", df["quantity"].cast(IntegerType()))

# Write to Delta table
df.write.format("delta").mode("append").partitionBy("added_at").save("abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/shopping_cart")

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, rand
from pyspark.sql.types import StringType, DateType, DecimalType
from faker import Faker
import datetime

# Initialize Faker
fake = Faker()

# Generate 1000 records
data = [(fake.uuid4(), fake.uuid4(), fake.date_between(start_date='-1y', end_date='today'), fake.pydecimal(left_digits=5, right_digits=2, positive=True), fake.random_element(elements=('Processing', 'Shipped', 'Delivered')), fake.uuid4(), fake.date_between(start_date='-1y', end_date='today')) for _ in range(1000)]

# Create DataFrame
df = spark.createDataFrame(data, ["order_id", "user_id", "order_date", "total", "status", "tracking_number", "shipping_date"])

df = df.withColumn("total", df["total"].cast(DecimalType(10, 2)))

# Write to Delta table
df.write.format("delta").mode("append").partitionBy("order_date").save("abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/orders")

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, rand
from pyspark.sql.types import StringType, IntegerType, DecimalType
from faker import Faker

# Initialize Faker
fake = Faker()

# Generate 1000 records
data = [(fake.uuid4(), fake.uuid4(), fake.uuid4(), fake.random_int(min=1, max=10), fake.pydecimal(left_digits=5, right_digits=2, positive=True)) for _ in range(1000)]

# Create DataFrame
df = spark.createDataFrame(data, ["order_item_id", "order_id", "product_id", "quantity", "price"])

df = df.withColumn("quantity", df["quantity"].cast(IntegerType()))

df = df.withColumn("price", df["price"].cast(DecimalType(10, 2)))

# Write to Delta table
df.write.format("delta").mode("append").partitionBy("order_id").save("abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/order_items")

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, rand
from pyspark.sql.types import StringType, DateType, DecimalType
from faker import Faker
import datetime

# Initialize Faker
fake = Faker()

# Generate 1000 records
data = [(fake.uuid4(), fake.uuid4(), fake.uuid4(), fake.pydecimal(left_digits=5, right_digits=2, positive=True), fake.date_between(start_date='-1y', end_date='today'), fake.random_element(elements=('Credit Card', 'Debit Card', 'PayPal')), fake.credit_card_number(card_type=None)) for _ in range(1000)]

# Create DataFrame
df = spark.createDataFrame(data, ["payment_id", "order_id", "user_id", "amount", "payment_date", "payment_method", "credit_card_id"])

df = df.withColumn("amount", df["amount"].cast(DecimalType(10, 2)))

# Write to Delta table
df.write.format("delta").mode("append").partitionBy("payment_date").save("abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/payments")

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, rand
from pyspark.sql.types import StringType, DateType, IntegerType
from faker import Faker
import datetime

# Initialize Faker
fake = Faker()

# Generate 1000 records
data = [(fake.uuid4(), fake.uuid4(), fake.credit_card_number(card_type=None), fake.date_between(start_date='today', end_date='+5y'), fake.random_int(min=100, max=999)) for _ in range(1000)]

# Create DataFrame
df = spark.createDataFrame(data, ["credit_card_id", "user_id", "card_number", "expiry_date", "cvv"])

# Write to Delta table
df.write.format("delta").mode("append").save("abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/credit_cards")

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, rand
from pyspark.sql.types import StringType, DateType, DecimalType
from faker import Faker
import datetime

# Initialize Faker
fake = Faker()

# Generate 1000 records
data = [(fake.uuid4(), fake.lexify(text='????????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'), fake.pydecimal(left_digits=2, right_digits=2, positive=True), fake.date_between(start_date='today', end_date='+1y')) for _ in range(1000)]

# Create DataFrame
df = spark.createDataFrame(data, ["coupon_id", "coupon_code", "discount", "expiry_date"])

df = df.withColumn("discount", df["discount"].cast(DecimalType(10, 2)))

# Write to Delta table
df.write.format("delta").mode("append").save("abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/coupons")

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, rand
from pyspark.sql.types import StringType
from faker import Faker

# Initialize Faker
fake = Faker()

# Generate 1000 records
data = [(fake.uuid4(), fake.company(), fake.address().replace('\n', ', ')) for _ in range(1000)]

# Create DataFrame
df = spark.createDataFrame(data, ["store_id", "store_name", "store_location"])

# Write to Delta table
df.write.format("delta").mode("append").save("abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/stores")

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DateType

# Define the ADLS file path for the CSV file
file_path = 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/data/users/Ecommerce_Users.csv'

# Define the schema explicitly to avoid conflicts
schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("username", StringType(), True),
    StructField("password", StringType(), True),
    StructField("email", StringType(), True),
    StructField("created_at", DateType(), True)
])

# Load the CSV file into a DataFrame with the defined schema
df = spark.read.schema(schema).csv(file_path, header=True)

# Define the Delta table path
delta_table_path = "abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/users"

# Write the DataFrame to the Delta table
df.write.format("delta").mode("overwrite").partitionBy("created_at").save(delta_table_path)



# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DecimalType, DateType

# Define the ADLS file path for the CSV file
file_path = 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/data/products/Ecommerce_Products.csv'

# Define the schema explicitly to avoid conflicts
schema = StructType([
    StructField("product_id", StringType(), True),
    StructField("product_name", StringType(), True),
    StructField("product_description", StringType(), True),
    StructField("category_id", StringType(), True),
    StructField("price", DecimalType(10, 2), True),
    StructField("created_at", DateType(), True)
])

# Load the CSV file into a DataFrame with the defined schema
df = spark.read.schema(schema).csv(file_path, header=True)

# Define the Delta table path
delta_table_path = "abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/products"

# Write the DataFrame to the Delta table
df.write.format("delta").mode("overwrite").partitionBy("created_at").save(delta_table_path)



# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType

# Define the ADLS file path for the CSV file
file_path = 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/data/categories/Ecommerce_Categories.csv'

# Define the schema explicitly to avoid conflicts
schema = StructType([
    StructField("category_id", StringType(), True),
    StructField("category_name", StringType(), True),
    StructField("category_groupname", StringType(), True)  # Including the additional column to load it but will not use it in the table
])

# Load the CSV file into a DataFrame with the defined schema
df = spark.read.schema(schema).csv(file_path, header=True)

# Define the Delta table path
delta_table_path = "abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/product_categories"

# Write the DataFrame to the Delta table
df.write.format("delta").mode("overwrite").save(delta_table_path)

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

# Define the ADLS file path for the CSV file
file_path = 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/data/shopping_cart/Ecommerce_Shopping_Cart.csv'

# Define the schema explicitly to avoid conflicts
schema = StructType([
    StructField("cart_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("added_at", DateType(), True)
])

# Load the CSV file into a DataFrame with the defined schema
df = spark.read.schema(schema).csv(file_path, header=True)

# Define the Delta table path
delta_table_path = "abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/shopping_cart"

# Write the DataFrame to the Delta table
df.write.format("delta").mode("overwrite").partitionBy("added_at").save(delta_table_path)




# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DecimalType, DateType

# Define the ADLS file path for the CSV file
file_path = 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/data/orders/Ecommerce_Orders.csv'

# Define the schema explicitly to avoid conflicts
schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("order_date", DateType(), True),
    StructField("total", DecimalType(10, 2), True),
    StructField("status", StringType(), True),
    StructField("tracking_number", StringType(), True),
    StructField("shipping_date", DateType(), True)
])

# Load the CSV file into a DataFrame with the defined schema
df = spark.read.schema(schema).csv(file_path, header=True)

# Define the Delta table path
delta_table_path = "abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/orders"

# Write the DataFrame to the Delta table
df.write.format("delta").mode("overwrite").partitionBy("order_date").save(delta_table_path)



# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DecimalType

# Define the ADLS file path for the CSV file
file_path = 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/data/order_items/Ecommerce_Order_Items.csv'

# Define the schema explicitly to avoid conflicts
schema = StructType([
    StructField("order_item_id", StringType(), True),
    StructField("order_id", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("price", DecimalType(10, 2), True)
])

# Load the CSV file into a DataFrame with the defined schema
df = spark.read.schema(schema).csv(file_path, header=True)

# Define the Delta table path
delta_table_path = "abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/order_items"

# Write the DataFrame to the Delta table
df.write.format("delta").mode("overwrite").partitionBy("order_id").save(delta_table_path)
