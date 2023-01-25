SELECT aurora_api.tree.path
FROM aurora_api.tree
     RIGHT JOIN aurora_api.metadata
     ON aurora_api.tree.meter_id = aurora_api.metadata.meter_id
     RIGHT JOIN aurora_api.building_counts
     ON aurora_api.metadata.building_id = aurora_api.building_counts.building_id
WHERE aurora_api.tree.path ~ CONCAT('*.', aurora_api.building_counts.building_id ,'.*')::LQUERY;
