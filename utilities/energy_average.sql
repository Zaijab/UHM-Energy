DELETE FROM aurora.power_average
WHERE meter_name LIKE '%KEY_PERF_IND';

WITH offending AS (SELECT s.datetime, truncated_meter_name
     FROM
	(SELECT datetime, RIGHT(LEFT(meter_name, -4), -3) AS truncated_meter_name
      	FROM aurora.power_average
      	WHERE meter_name LIKE '%_GIM') s
      	INNER JOIN aurora.power_average
      	    ON aurora.power_average.datetime = s.datetime AND
      	       aurora.power_average.meter_name = s.truncated_meter_name)
DELETE FROM aurora.power_average
USING offending
WHERE aurora.power_average.datetime = offending.datetime AND aurora.power_average.meter_name = offending.truncated_meter_name;

UPDATE aurora.power_average
SET meter_name = RIGHT(LEFT(meter_name, -4), -3)
WHERE meter_name LIKE '%_GIM';
