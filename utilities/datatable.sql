CREATE OR REPLACE VIEW aurora_api.building_power_average AS
SELECT aurora_api.building_counts.building AS building_name,
       aurora.power_average.datetime AS datetime,
       SUM(aurora.power_average.kw_average) AS kw_average,
       MAX(weather.frog.temperature_c) AS temperature_c,
       MAX(weather.frog."humidity_%") AS humidity,
       MAX(weather.frog.solar_radiation_wm2) AS solar_radiation_wm2,
       MAX(calendar.timestamp.day_type) AS day_type
FROM aurora.power_average
     INNER JOIN weather.frog
     ON aurora.power_average.datetime = weather.frog.datetime
     INNER JOIN calendar.timestamp
     ON aurora.power_average.datetime = calendar.timestamp.datetime
     RIGHT JOIN aurora_api.metadata
     ON aurora.power_average.meter_name = aurora_api.metadata.meter_name
     RIGHT JOIN aurora_api.building_counts
     ON aurora_api.metadata.building_id = aurora_api.building_counts.building_id
GROUP BY aurora_api.building_counts.building, aurora.power_average.datetime
HAVING COUNT(aurora.power_average.meter_name) = MAX(aurora_api.building_counts.meter_count)
ORDER BY aurora_api.building_counts.building, aurora.power_average.datetime;
