# Databricks notebook source
# MAGIC %md
# MAGIC Sales Reports: These reports provide insights into total sales, sales by product category, sales by region, daily or monthly sales, etc. They help in understanding which products are performing well and which are not.

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog `ecomm-app-insights-dev-westus-databricks-catalog`

# COMMAND ----------

# MAGIC %sql
# MAGIC use schema `bronze`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DATE_TRUNC('day', order_date) AS order_date, 
# MAGIC        COUNT(DISTINCT order_id) AS number_of_orders, 
# MAGIC        SUM(quantity * price) AS total_sales
# MAGIC FROM order_history 
# MAGIC JOIN products ON order_history.product_id = products.product_id
# MAGIC GROUP BY DATE_TRUNC('day', order_date)
# MAGIC ORDER BY order_date DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ###Total Sales Report: This report gives the total sales amount.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT SUM(oi.price * oi.quantity) AS total_sales
# MAGIC FROM order_items oi;

# COMMAND ----------

# MAGIC %md
# MAGIC ###Sales by Product Category Report: This report gives the total sales amount for each product category.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT pc.category_name, SUM(oi.price * oi.quantity) AS total_sales
# MAGIC FROM order_items oi
# MAGIC JOIN products p ON oi.product_id = p.product_id
# MAGIC JOIN product_categories pc ON p.category_id = pc.category_id
# MAGIC GROUP BY pc.category_name;

# COMMAND ----------

# MAGIC %md
# MAGIC ###Sales by Region Report: This report gives the total sales amount for each store location (assuming store location is equivalent to region).

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT s.store_location, SUM(oi.price * oi.quantity) AS total_sales
# MAGIC FROM order_items oi
# MAGIC JOIN orders o ON oi.order_id = o.order_id
# MAGIC JOIN users u ON o.user_id = u.user_id
# MAGIC JOIN stores s ON u.user_id = s.store_id
# MAGIC GROUP BY s.store_location;

# COMMAND ----------

# MAGIC %md
# MAGIC ###Daily Sales Report: This report gives the total sales amount for each day.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DATE(o.order_date) AS sale_date, SUM(oi.price * oi.quantity) AS total_sales
# MAGIC FROM order_items oi
# MAGIC JOIN orders o ON oi.order_id = o.order_id
# MAGIC GROUP BY DATE(o.order_date)
# MAGIC ORDER BY DATE(o.order_date) DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ###Monthly Sales Report: This report gives the total sales amount for each month.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT CONCAT(EXTRACT(YEAR FROM o.order_date), '-', LPAD(EXTRACT(MONTH FROM o.order_date), 2, '0')) AS sale_month, SUM(oi.price * oi.quantity) AS total_sales
# MAGIC FROM order_items oi
# MAGIC JOIN orders o ON oi.order_id = o.order_id
# MAGIC GROUP BY CONCAT(EXTRACT(YEAR FROM o.order_date), '-', LPAD(EXTRACT(MONTH FROM o.order_date), 2, '0'))
# MAGIC ORDER BY CONCAT(EXTRACT(YEAR FROM o.order_date), '-', LPAD(EXTRACT(MONTH FROM o.order_date), 2, '0')) DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC Customer Behavior Reports: These reports analyze the behavior of customers on the website, such as most viewed products, products added to cart but not purchased, time spent on the website, pages visited, etc.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT product_id, 
# MAGIC        COUNT(DISTINCT user_id) AS number_of_users_viewed
# MAGIC FROM website_traffic 
# MAGIC WHERE page_visited LIKE '%product%'
# MAGIC GROUP BY product_id
# MAGIC ORDER BY number_of_users_viewed DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ###Most Viewed Products Report: This report gives the most viewed products. You can use the product_views table to track this.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT p.product_id, p.product_name, COUNT(*) as view_count
# MAGIC FROM product_views pv
# MAGIC JOIN products p ON pv.product_id = p.product_id
# MAGIC GROUP BY p.product_id, p.product_name
# MAGIC ORDER BY view_count DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ###Products Added to Cart But Not Purchased Report: This report gives the products that were added to the cart but not purchased.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT p.product_id, p.product_name
# MAGIC FROM shopping_cart sc
# MAGIC LEFT JOIN orders o ON sc.user_id = o.user_id AND sc.product_id = o.product_id
# MAGIC JOIN products p ON sc.product_id = p.product_id
# MAGIC WHERE o.order_id IS NULL;

# COMMAND ----------

# MAGIC %md
# MAGIC ###Time Spent on the Website Report: This report gives the time spent on the website. You can use the user_sessions table to track this.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT us.user_id, SUM(DATEDIFF(MINUTE, us.session_start, us.session_end)) as total_time_spent
# MAGIC FROM user_sessions us
# MAGIC GROUP BY us.user_id;

# COMMAND ----------

# MAGIC %md
# MAGIC ###Pages Visited Report: This report gives the pages visited by the user. You can use the page_visits table to track this.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT pv.user_id, pv.page_url, COUNT(*) as visit_count
# MAGIC FROM page_visits pv
# MAGIC GROUP BY pv.user_id, pv.page_url
# MAGIC ORDER BY visit_count DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC Inventory Reports: These reports provide information about the stock levels of different products. They can help in identifying which products are about to run out of stock and which products are overstocked.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT product_id, 
# MAGIC        quantity AS stock_level
# MAGIC FROM inventory
# MAGIC ORDER BY quantity ASC;

# COMMAND ----------

# MAGIC %md
# MAGIC Customer Segmentation Reports: These reports divide the customers into different segments based on various factors like age, location, buying behavior, etc. They can help in personalizing the marketing efforts for different segments of customers.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT location, 
# MAGIC        COUNT(DISTINCT user_id) AS number_of_users
# MAGIC FROM users
# MAGIC GROUP BY location
# MAGIC ORDER BY number_of_users DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC Marketing Campaign Performance Reports: These reports analyze the performance of various marketing campaigns. They can provide insights into which marketing campaigns are working and which are not.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT campaign_id, 
# MAGIC        COUNT(DISTINCT user_id) AS number_of_users_reached, 
# MAGIC        SUM(case when order_id is not null then 1 else 0 end) AS number_of_orders
# MAGIC FROM marketing_campaigns 
# MAGIC LEFT JOIN order_history ON marketing_campaigns.user_id = order_history.user_id
# MAGIC GROUP BY campaign_id
# MAGIC ORDER BY number_of_orders DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC Website Traffic Reports: These reports provide information about the traffic on the website. They can provide insights into peak traffic times, sources of traffic, bounce rates, etc.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DATE_TRUNC('hour', visit_time) AS visit_hour, 
# MAGIC        COUNT(DISTINCT session_id) AS number_of_sessions
# MAGIC FROM website_traffic
# MAGIC GROUP BY DATE_TRUNC('hour', visit_time)
# MAGIC ORDER BY visit_hour DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC Conversion Rate Reports: These reports analyze the conversion rate of the website, i.e., the percentage of visitors who make a purchase. They can help in identifying issues in the conversion funnel and improving the conversion rate.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(DISTINCT case when order_id is not null then user_id else null end) * 1.0 / COUNT(DISTINCT user_id) AS conversion_rate
# MAGIC FROM website_traffic
# MAGIC LEFT JOIN order_history ON website_traffic.user_id = order_history.user_id;

# COMMAND ----------

# MAGIC %md
# MAGIC Customer Retention Reports: These reports analyze the retention rate of customers, i.e., the percentage of customers who make repeat purchases. They can help in understanding customer loyalty and identifying ways to improve customer retention.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT user_id, 
# MAGIC        COUNT(DISTINCT order_id) AS number_of_orders
# MAGIC FROM order_history
# MAGIC GROUP BY user_id
# MAGIC HAVING COUNT(DISTINCT order_id) > 1;

# COMMAND ----------

# MAGIC %md
# MAGIC Profitability Reports: These reports provide information about the profitability of the business. They can help in understanding the cost of goods sold, operating expenses, net profit, etc.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DATE_TRUNC('month', order_date) AS order_month, 
# MAGIC        SUM(quantity * price) AS total_sales, 
# MAGIC        SUM(quantity * cost) AS total_cost, 
# MAGIC        (SUM(quantity * price) - SUM(quantity * cost)) AS profit
# MAGIC FROM order_history 
# MAGIC JOIN products ON order_history.product_id = products.product_id
# MAGIC GROUP BY DATE_TRUNC('month', order_date)
# MAGIC ORDER BY order_month DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC Order Fulfillment Reports: These reports provide insights into the order fulfillment process, such as average time to fulfill an order, percentage of orders fulfilled on time, etc.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT order_id, 
# MAGIC        DATEDIFF(day, order_date, shipping_date) AS fulfillment_days
# MAGIC FROM order_history 
# MAGIC JOIN shipping ON order_history.order_id = shipping.order_id;
