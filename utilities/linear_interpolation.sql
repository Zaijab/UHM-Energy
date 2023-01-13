CREATE TABLE interpolated_energy_actual AS
WITH dense AS (
     SELECT generate_series AS datetime,
            s.meter_name
     FROM generate_series(TO_TIMESTAMP('2022-01-00 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
                          TO_TIMESTAMP('2022-12-31 23:45:00', 'YYYY-MM-DD HH24:MI:SS'), '15 min') CROSS JOIN
       (SELECT DISTINCT(aurora.energy_actual.meter_name) FROM aurora.energy_actual) s)
SELECT * FROM
(SELECT dense.datetime,
       dense.meter_name,
       aurora.energy_actual.kwh_actual,
       COALESCE(kwh_actual,
       aurora_api.linear_interpolate(dense.datetime::timestamp,
                                     (aurora_api.last_known(energy_actual.datetime) OVER lookback)::timestamp,
				     aurora_api.last_known(kwh_actual) OVER lookback,
				     (aurora_api.last_known(energy_actual.datetime) OVER lookforward)::timestamp,
				     aurora_api.last_known(kwh_actual) OVER lookforward)) AS interpolated
FROM aurora.energy_actual RIGHT JOIN DENSE
     ON energy_actual.meter_name = dense.meter_name AND energy_actual.datetime = dense.datetime
WINDOW
lookback AS (PARTITION BY dense.meter_name ORDER BY dense.datetime),
lookforward AS (PARTITION BY dense.meter_name ORDER BY dense.datetime DESC)
ORDER BY dense.meter_name, dense.datetime) q
WHERE q.interpolated IS NOT NULL;
