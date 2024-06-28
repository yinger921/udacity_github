 
/* Question1-query used for first insight  (Visualization 1) */

SELECT 
     f.title AS Film_title, 
     c.name AS Category_name, 
    COUNT(r.rental_id) AS Count_of_Rentals
FROM Film f
JOIN Film_Category fc 
ON f.film_id=fc.film_id
JOIN Category c 
ON fc.category_id = c.category_id
JOIN Inventory i 
ON f.film_id= i.film_id
JOIN Rental r 
ON r.inventory_id=i.inventory_id
WHERE 
 c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')
 GROUP BY f.title, c.name
 ORDER BY c.name, f.title;


/*Question1-query used for second insight  (Visualization 2) */

WITH MoviesDuration AS (
    SELECT
        f.title AS film_title,
        c.name AS category_name,
        f.rental_duration,
        NTILE(4) OVER (ORDER BY f.rental_duration) AS rental_duration_quartile
    FROM 
        film f
    JOIN 
        film_category fc ON f.film_id = fc.film_id
    JOIN 
        category c ON fc.category_id = c.category_id
    WHERE
        c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')
),
AllMoviesQuartiles AS (
    SELECT
        film_title,
        category_name,
        rental_duration,
        CASE
            WHEN rental_duration_quartile = 1 THEN '1'
            WHEN rental_duration_quartile = 2 THEN '2'
            WHEN rental_duration_quartile = 3 THEN '3'
            WHEN rental_duration_quartile = 4 THEN '4'
        END AS rental_duration_category
    FROM
        MoviesDuration
)
SELECT 
    category_name AS "Category",
    rental_duration_category AS "Rental length category",
    COUNT(film_title) AS "Count"
FROM
    AllMoviesQuartiles
GROUP BY
    category_name, rental_duration_category
ORDER BY
    category_name, rental_duration_category;


/*Question2-query used for first insight (Visualization 3) */ 
SELECT 
    EXTRACT(MONTH FROM r.rental_date) AS month,
    EXTRACT(YEAR FROM r.rental_date) AS year,
    s.store_id AS store_ID,
    COUNT(r.rental_id) AS rental_count
FROM 
    rental r
JOIN store s ON s.manager_staff_id= r.staff_id
GROUP BY 
    store_id, 
    EXTRACT(MONTH FROM r.rental_date),
    EXTRACT(YEAR FROM r.rental_date)
ORDER BY 
     year,
     rental_count DESC;

/* Question2-query used for second insight (Visualization 4) */ 
/* Subquery to find the top 10 paying customers */
WITH TopCustomers AS (
    SELECT 
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        SUM(p.amount) AS total_amount
    FROM 
        payment p
    JOIN 
        customer c 
   ON p.customer_id = c.customer_id
    WHERE 
        EXTRACT(YEAR FROM p.payment_date) = 2007
    GROUP BY 
        c.customer_id, c.first_name, c.last_name
    ORDER BY 
        total_amount DESC
    LIMIT 10
)

/* Main query to get the monthly payment details for these top customers */
SELECT 
    EXTRACT(MONTH FROM p.payment_date) AS pay_mon,
    tc.customer_name AS fullname,
    COUNT(p.payment_id) AS pay_countpermon,
    SUM(p.amount) AS pay_amount
FROM 
    payment p
JOIN 
    TopCustomers tc 
ON p.customer_id = tc.customer_id
WHERE 
    EXTRACT(YEAR FROM p.payment_date) = 2007
GROUP BY 
   tc.customer_name,  pay_mon
ORDER BY 
    tc.customer_name, pay_mon;


 