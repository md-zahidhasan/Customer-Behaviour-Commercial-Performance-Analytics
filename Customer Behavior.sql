CREATE TABLE events_clean AS
SELECT
    customer_id,
    event,
	time,
    -- Extract offer_id
    CASE
        WHEN value LIKE '%offer id%' THEN
            REPLACE(REPLACE(SUBSTR(value, INSTR(value, ':') + 3, LENGTH(value) - INSTR(value, ':') - 3), '''', ''), '}', '')
        WHEN value LIKE '%offer_id%' THEN
            REPLACE(REPLACE(SUBSTR(value, INSTR(value, ':') + 3, INSTR(value, ',') - INSTR(value, ':') - 3), '''', ''), '}', '')
        ELSE NULL
    END AS offer_id,

    -- Extract amount
    CASE
        WHEN value LIKE '%amount%' THEN
            CAST(REPLACE(REPLACE(REPLACE(value, '{''amount'': ', ''), '}', ''), '''', '') AS FLOAT)
        ELSE NULL
    END AS amount,

    -- Extract reward
    CASE
        WHEN value LIKE '%reward%' THEN
            CAST(SUBSTR(value, INSTR(value, 'reward') + 9, LENGTH(value) - INSTR(value, 'reward') - 8) AS FLOAT)
        ELSE NULL
    END AS reward

FROM events;


SELECT * FROM events_clean

SELECT * FROM events_clean WHERE event = 'offer completed'

--------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------
-- offer
-- 1. Number of offers by offer type

SELECT offer_type, COUNT(*) AS total_offer_types
FROM offers
GROUP BY offer_type;


-- 2. Average reward and avg_spending by offer type

SELECT offer_type, AVG(difficulty) AS avg_spend , AVG(reward) AS avg_reward
FROM offers
GROUP BY offer_type;

-- 3. Average Income by Gender

SELECT gender, round(AVG(income),1) AS avg_income
FROM customers
GROUP BY gender;

-- Events
-- 4.Total Transactions & Revenue Earned
SELECT 
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue , SUM(amount)/ COUNT(*) as avg_spend
FROM events_clean
WHERE event = 'transaction'; 


-- 5. Identifies high-value loyalty customers.
SELECT 
    customer_id,
    SUM(amount) AS total_spent,
    SUM(reward) AS total_rewards,
	RANK() OVER (ORDER BY SUM(amount) DESC) AS spend_rank
FROM events_clean
GROUP BY customer_id
ORDER BY spend_rank 


-- 6. Which offer type was pushed the most?
SELECT o.offer_type, COUNT(e.offer_id) AS offers_sent
FROM events_clean e
JOIN offers o ON e.offer_id = o.offer_id
WHERE e.event = 'offer received'
GROUP BY o.offer_type


-- 7. Average Transaction Value by Age Group
SELECT 
    CASE 
        WHEN age < 25 THEN '18-24'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 50 THEN '35-50'
        ELSE '50+'
    END AS age_group,
    round(AVG(amount),1) AS avg_spend
FROM customers c
JOIN events_clean e ON c.customer_id = e.customer_id
WHERE e.event = 'transaction'
GROUP BY age_group;



































SELECT   CASE 
        WHEN age < 25 THEN '18-24'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 50 THEN '35-50'
        ELSE '50+'
    END AS age_group,
    round(AVG(amount),1) AS avg_spend
FROM customers c
JOIN events_clean e ON c.customer_id = e.customer_id
WHERE e.event = 'transaction'
GROUP BY age_group;

























