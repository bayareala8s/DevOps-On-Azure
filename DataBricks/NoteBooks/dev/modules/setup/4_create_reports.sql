-- Databricks notebook source
use catalog `ecomm-app-insights-dev-westus-databricks-catalog`

-- COMMAND ----------

use schema `bronze`

-- COMMAND ----------

SHOW TABLES IN bronze

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###User Growth Over Time
-- MAGIC This report shows the number of new users registered over time.

-- COMMAND ----------

SELECT
  created_at,
  COUNT(user_id) AS new_users
FROM users
GROUP BY created_at
ORDER BY created_at;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###Sales by Product Category
-- MAGIC This report shows the total sales amount for each product category.

-- COMMAND ----------

SELECT
  pc.category_name,
  SUM(oi.price * oi.quantity) AS total_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN product_categories pc ON p.category_id = pc.category_id
GROUP BY pc.category_name
ORDER BY total_sales DESC;

-- COMMAND ----------

-- Creating a temporary table for a random category
CREATE OR REPLACE TEMP VIEW random_category AS
SELECT category_id
FROM product_categories
ORDER BY RAND()
LIMIT 1;


-- COMMAND ----------

-- Creating a temporary table for random product IDs
CREATE OR REPLACE TEMP VIEW random_products AS
SELECT product_id
FROM products
ORDER BY RAND()
LIMIT 150;


-- COMMAND ----------

-- Create a view with updated category_id for selected product_ids
CREATE OR REPLACE TEMP VIEW updated_products AS
SELECT
  p.product_id,
  rc.category_id
FROM
  products p
JOIN
  random_products rp
  ON p.product_id = rp.product_id
CROSS JOIN
  random_category rc;

-- Update the products table using the updated_products view
MERGE INTO products AS p
USING updated_products AS u
ON p.product_id = u.product_id
WHEN MATCHED THEN
UPDATE SET
  p.category_id = u.category_id;


-- COMMAND ----------

SELECT 
    p.product_id,
    p.product_name,
    p.product_description,
    p.category_id,
    c.category_name,
    p.price,
    p.created_at
FROM 
    products p
INNER JOIN 
    product_categories c
ON 
    p.category_id = c.category_id;


-- COMMAND ----------

SELECT
  *
FROM product_categories pc

-- COMMAND ----------

-- Creating a temporary view for random product IDs
CREATE OR REPLACE TEMP VIEW random_products AS
SELECT product_id
FROM products
ORDER BY RAND()
LIMIT 5;


-- COMMAND ----------

select * from random_products

-- COMMAND ----------

-- Creating a temporary view with row numbers for random product IDs
CREATE OR REPLACE TEMP VIEW random_products_with_row_num AS
SELECT product_id, ROW_NUMBER() OVER (ORDER BY product_id) AS row_num
FROM random_products;

-- Creating a temporary view with row numbers for order items to be updated
CREATE OR REPLACE TEMP VIEW order_items_with_row_num AS
SELECT order_item_id, ROW_NUMBER() OVER (ORDER BY order_item_id) AS row_num
FROM order_items
ORDER BY RAND()
LIMIT 5;


-- COMMAND ----------

select * from random_products_with_row_num

-- COMMAND ----------

select * from order_items_with_row_num

-- COMMAND ----------

-- Creating a temporary view to map random product IDs to order item IDs
CREATE OR REPLACE TEMP VIEW order_items_to_update AS
SELECT 
  oi.order_item_id,
  rp.product_id
FROM 
  order_items_with_row_num oi
JOIN
  random_products_with_row_num rp
ON
  oi.row_num = rp.row_num;


-- COMMAND ----------

-- Updating the order_items table using the order_items_to_update view
MERGE INTO order_items AS oi
USING order_items_to_update AS ou
ON oi.order_item_id = ou.order_item_id
WHEN MATCHED THEN
UPDATE SET
  oi.product_id = ou.product_id;


-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###Top-Selling Products
-- MAGIC This report lists the top 10 best-selling products by quantity sold.

-- COMMAND ----------

SELECT
  p.product_name,
  SUM(oi.quantity) AS total_quantity
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_quantity DESC
LIMIT 10;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###Customer Lifetime Value (CLV)
-- MAGIC This report calculates the total amount spent by each customer.

-- COMMAND ----------

SELECT
  u.user_id,
  u.username,
  SUM(o.total) AS total_spent
FROM users u
JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.username
ORDER BY total_spent DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###Order Fulfillment Time
-- MAGIC This report shows the average time taken to fulfill orders.

-- COMMAND ----------

SELECT
  AVG(DATEDIFF(shipping_date, order_date)) AS avg_fulfillment_time
FROM orders
WHERE shipping_date IS NOT NULL;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###Revenue Over Time
-- MAGIC This report shows the total revenue generated over time.

-- COMMAND ----------

SELECT
  order_date,
  SUM(total) AS total_revenue
FROM orders
GROUP BY order_date
ORDER BY order_date;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###Product Views by User
-- MAGIC This report shows the number of times each user viewed products.

-- COMMAND ----------

SELECT
  u.user_id,
  u.username,
  COUNT(pv.view_id) AS total_views
FROM users u
JOIN product_views pv ON u.user_id = pv.user_id
GROUP BY u.user_id, u.username
ORDER BY total_views DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###Conversion Rate
-- MAGIC This report calculates the conversion rate (percentage of users who made a purchase) for the site.

-- COMMAND ----------

-- MAGIC %python
-- MAGIC WITH user_sessions AS (
-- MAGIC   SELECT DISTINCT user_id FROM user_sessions
-- MAGIC ),
-- MAGIC users_with_orders AS (
-- MAGIC   SELECT DISTINCT user_id FROM orders
-- MAGIC )
-- MAGIC SELECT
-- MAGIC   (SELECT COUNT(*) FROM users_with_orders) / (SELECT COUNT(*) FROM user_sessions) * 100 AS conversion_rate;
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###Most Used Coupons
-- MAGIC This report lists the most frequently used coupons and their total discount amount.

-- COMMAND ----------

SELECT
  c.coupon_code,
  COUNT(o.order_id) AS usage_count,
  SUM(c.discount) AS total_discount
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN coupons c ON p.product_id = c.coupon_id
GROUP BY c.coupon_code
ORDER BY usage_count DESC, total_discount DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###Shopping Cart Abandonment Rate
-- MAGIC This report calculates the shopping cart abandonment rate.

-- COMMAND ----------

-- MAGIC %python
-- MAGIC WITH carts AS (
-- MAGIC   SELECT DISTINCT cart_id, user_id FROM shopping_cart
-- MAGIC ),
-- MAGIC carts_with_orders AS (
-- MAGIC   SELECT DISTINCT sc.cart_id
-- MAGIC   FROM shopping_cart sc
-- MAGIC   JOIN orders o ON sc.user_id = o.user_id
-- MAGIC )
-- MAGIC SELECT
-- MAGIC   (SELECT COUNT(*) FROM carts WHERE cart_id NOT IN (SELECT cart_id FROM carts_with_orders)) / (SELECT COUNT(*) FROM carts) * 100 AS abandonment_rate;
-- MAGIC
