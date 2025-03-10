with 
b_exchange_rates AS
(
    SELECT * FROM "WH_LF"."bronze"."b_exchange_rates"
),

cast_rows AS
(
    SELECT
        CAST(Date AS DATE) AS exchange_date
        ,currency_cd
        ,currency_nm
        ,CAST(CAST(exchange_rt AS DECIMAL(10,2)) AS INT) AS exchange_rt
        ,CAST(exchange_amt AS DECIMAL(8,2)) AS exchange_amt
    FROM b_exchange_rates
),

calc_exchange_rates AS
(
    SELECT
        exchange_date
        ,currency_cd
        ,currency_nm
        ,CAST(exchange_amt / exchange_rt AS DECIMAL(8,2)) AS exchange_amt
    FROM cast_rows
)

SELECT
*
FROM calc_exchange_rates