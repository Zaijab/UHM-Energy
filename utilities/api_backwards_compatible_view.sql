/*
      datetime       |       meter_name        |     kw_average     
---------------------+-------------------------+--------------------
 2021-07-01 00:00:00 | kW_ADMIN_SERV_1_MTR_GIM | 11.055417330000004
 2021-07-01 00:15:00 | kW_ADMIN_SERV_1_MTR_GIM | 17.567561204444445
 2021-07-01 00:30:00 | kW_ADMIN_SERV_1_MTR_GIM | 20.257477388888887
 2021-07-01 00:45:00 | kW_ADMIN_SERV_1_MTR_GIM | 20.600283022222225
*/

CREATE OR REPLACE VIEW aurora_api.power_average_backwards_compatible AS
SELECT "SiteDateTime" AS datetime,
       "Entity" AS meter_name,
       "Mean" AS kw_average
FROM aurora_api.kw
     INNER JOIN aurora_api.meters
     ON aurora_api.kw."TagId"=aurora_api.meters."Id";

CREATE OR REPLACE VIEW aurora_api.energy_average_backwards_compatible AS
SELECT "SiteDateTime" AS datetime,
       "Entity" AS meter_name,
       "Mean" AS kw_average
FROM aurora_api.kwh
     INNER JOIN aurora_api.meters
     ON aurora_api.kwh."TagId"=aurora_api.meters."Id";

