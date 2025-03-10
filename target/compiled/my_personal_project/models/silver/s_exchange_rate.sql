with 
cast_rows AS
(
SELECT
    CAST(Date AS DATE) AS exchange_date
    ,currency_cd
    ,currency_nm
    ,CAST(exchange_rt AS INT) AS exchange_rt
    ,CAST(exchange_amt AS DECIMAL(8,2)) AS exchange_date
FROM bronze.b_exchange_rate
)

SELECT
*
FROM cast_rows