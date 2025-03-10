
  
    
    
    

    EXEC('CREATE TABLE "WH_LF"."bronze"."b_exchange_rates__dbt_temp" AS SELECT 
    Date,
    [0] AS currency_cd,
    [1] AS currency_nm,
    [2] AS exchange_rt,
    [3] AS exchange_amt
FROM LH_LF.dbo.ld_exchange_rates 
    OPTION (LABEL = ''dbt-fabric-dw'');
');

    

  
  