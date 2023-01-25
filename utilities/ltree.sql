CREATE OR REPLACE VIEW aurora_api.metadata AS
SELECT "Filter_Name" AS unit,
       "Entity" AS meter_name,
       replace("Id",'-','') AS meter_id,
       "Building" AS building,
       md5("Building") AS building_id,
       "SiteName" AS campus,
       replace("SiteId",'-','') AS campus_id
FROM aurora_api.meters
WHERE "Entity" NOT LIKE '%KEY_PERF%' AND
      "SiteId" SIMILAR TO '%[a-zA-Z0-9]%' AND
      "Building" SIMILAR TO '%[a-zA-Z0-9]%' AND
      "Id" SIMILAR TO '%[a-zA-Z0-9]%' AND
      "Filter_Name" = 'AllkW';

CREATE MATERIALIZED VIEW  aurora_api.tree AS
SELECT meter_id AS meter_id,
       text2ltree(campus_id || '.' || building_id || '.' || meter_id) AS path
FROM aurora_api.metadata;

CREATE OR REPLACE VIEW aurora_api.building_counts AS
SELECT building, max(building_id) AS building_id, count(meter_name) AS meter_count
FROM aurora_api.metadata
GROUP BY building;
