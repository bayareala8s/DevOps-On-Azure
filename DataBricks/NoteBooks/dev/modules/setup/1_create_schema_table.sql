-- Databricks notebook source
-- MAGIC %md
-- MAGIC ###The ecomm-app-insights-dev-westus-databricks-catalog is a Unity Catalog used for organizing, managing, and securing data assets in the e-commerce application insights development environment located in the West US region on Databricks. It helps streamline data governance and collaboration across different teams and projects within the organization.
-- MAGIC
-- MAGIC ####Key Features
-- MAGIC Data Organization:
-- MAGIC Provides a hierarchical namespace for organizing data assets, including catalogs, schemas, and tables.
-- MAGIC Facilitates the logical grouping of data for better management and accessibility.
-- MAGIC
-- MAGIC Data Management:
-- MAGIC Allows the creation, modification, and deletion of data assets such as tables, views, and functions.
-- MAGIC Supports Delta Lake tables for efficient data processing and analytics.
-- MAGIC
-- MAGIC Data Governance:
-- MAGIC Enables fine-grained access control to data assets using role-based access controls (RBAC).
-- MAGIC Ensures data security and compliance with organizational policies and regulatory requirements.
-- MAGIC
-- MAGIC Collaboration:
-- MAGIC Promotes collaboration by providing a shared workspace where data engineers, data scientists, and analysts can access and work with the same data.
-- MAGIC Integrates with Git for version control and collaborative development.
-- MAGIC
-- MAGIC Audit and Lineage:
-- MAGIC Tracks data access and modification activities for audit purposes.
-- MAGIC Provides data lineage information to understand the flow and transformation of data across the platform.

-- COMMAND ----------

use catalog `ecomm-app-insights-dev-westus-databricks-catalog`

-- COMMAND ----------

CREATE SCHEMA IF NOT EXISTS `bronze`
MANAGED LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/';

-- COMMAND ----------

CREATE SCHEMA IF NOT EXISTS `silver`
MANAGED LOCATION 'abfss://silver@ecommappinsightsdevadls.dfs.core.windows.net/';

-- COMMAND ----------

CREATE SCHEMA IF NOT EXISTS `gold`
MANAGED LOCATION 'abfss://gold@ecommappinsightsdevadls.dfs.core.windows.net/';

-- COMMAND ----------

use schema `bronze`

-- COMMAND ----------

-- Users table
CREATE TABLE users (
  user_id STRING,
  username STRING,
  password STRING,
  email STRING,
  created_at DATE
)
USING delta
PARTITIONED BY (created_at)
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/users';

-- COMMAND ----------

-- Products table
CREATE TABLE products (
  product_id STRING,
  product_name STRING,
  product_description STRING,
  category_id STRING,
  price DECIMAL(10, 2),
  created_at DATE
)
USING delta
PARTITIONED BY (created_at)
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/products';

-- COMMAND ----------

DESCRIBE TABLE product_categories

-- COMMAND ----------

-- Product Categories table
CREATE TABLE product_categories (
  category_id STRING,
  category_name STRING
)
USING delta
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/product_categories';

-- COMMAND ----------

-- Add the new column
ALTER TABLE product_categories ADD COLUMNS (category_groupname STRING);

-- COMMAND ----------

-- Shopping Cart table
CREATE TABLE shopping_cart (
  cart_id STRING,
  user_id STRING,
  product_id STRING,
  quantity INT,
  added_at DATE
)
USING delta
PARTITIONED BY (added_at)
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/shopping_cart';

-- COMMAND ----------

-- Orders table
CREATE TABLE orders (
  order_id STRING,
  user_id STRING,
  order_date DATE,
  total DECIMAL(10, 2),
  status STRING,
  tracking_number STRING,
  shipping_date DATE
)
USING delta
PARTITIONED BY (order_date)
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/orders';

-- COMMAND ----------

-- Order items table
CREATE TABLE order_items (
  order_item_id STRING,
  order_id STRING,
  product_id STRING,
  quantity INT,
  price DECIMAL(10, 2)
)
USING delta
PARTITIONED BY (order_id)
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/order_items';

-- COMMAND ----------

-- Payment table
CREATE TABLE payments (
  payment_id STRING,
  order_id STRING,
  user_id STRING,
  amount DECIMAL(10, 2),
  payment_date DATE,
  payment_method STRING,
  credit_card_id STRING
)
USING delta
PARTITIONED BY (payment_date)
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/payments';

-- COMMAND ----------

-- Credit Cards table
CREATE TABLE credit_cards (
  credit_card_id STRING,
  user_id STRING,
  card_number STRING,
  expiry_date DATE,
  cvv INT
)
USING delta
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/credit_cards';

-- COMMAND ----------

-- Coupons table
CREATE TABLE coupons (
  coupon_id STRING,
  coupon_code STRING,
  discount DECIMAL(10, 2),
  expiry_date DATE
)
USING delta
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/coupons';

-- COMMAND ----------

-- Stores table
CREATE TABLE stores (
  store_id STRING,
  store_name STRING,
  store_location STRING
)
USING delta
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/stores';

-- COMMAND ----------

CREATE TABLE order_history (
  order_id STRING,
  user_id STRING,
  order_date DATE,
  order_status STRING,
  total_amount DECIMAL(10, 2)
)
USING delta
PARTITIONED BY (order_date)
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/order_history';

-- COMMAND ----------

CREATE TABLE product_views (
  view_id STRING,
  user_id STRING,
  product_id STRING,
  viewed_at DATE
)
USING delta
PARTITIONED BY (viewed_at)
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/product_views';

-- COMMAND ----------

CREATE TABLE user_sessions (
  session_id STRING,
  user_id STRING,
  session_start DATE,
  session_end DATE
)
USING delta
PARTITIONED BY (session_start, session_end)
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/user_sessions';

-- COMMAND ----------

CREATE TABLE page_visits (
  visit_id STRING,
  user_id STRING,
  page_url STRING,
  visited_at DATE
)
USING delta
PARTITIONED BY (visited_at)
LOCATION 'abfss://bronze@ecommappinsightsdevadls.dfs.core.windows.net/page_visits';
