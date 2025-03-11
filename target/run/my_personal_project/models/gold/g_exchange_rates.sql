
  
    
    
    

    EXEC('CREATE TABLE "WH_LF"."gold"."g_exchange_rates__dbt_temp" AS /* load the silver layer*/
SELECT * FROM "WH_LF"."silver"."s_exchange_rates" 
    OPTION (LABEL = ''dbt-fabric-dw'');
');

    

  
  