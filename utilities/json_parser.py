import pandas as pd
import json
import os
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

pd.options.display.max_columns = 999

with open('../data/bluepillar/filters.json', 'r') as filter_file:
    meters = pd.json_normalize(json.load(filter_file),
                                record_path=["Tags"],
                                meta=["Id", "Name"],
                                meta_prefix = "Filter_")

print
meters = meters[~meters["Building"].isna()]
sites = meters.groupby("SiteName").first().drop(columns=["Building", "Floor", "Room", "DataType", "Filter_Id", "Filter_Name", "Entity", "Name", "Id"])
buildings = meters.groupby("Building").first().drop(columns=["Filter_Name", "Filter_Id", "DataType", "Room", "Floor", "SiteName", "Entity", "Name", "Id"])

sites = sites.reset_index().rename(columns={"SiteName":"site_name", "SiteId":"site_id"})
buildings = buildings.reset_index().rename(columns={"Building":"building_name", "SiteId":"site_id"})
buildings["building_id"] = pd.util.hash_pandas_object(buildings["building_name"])
meters["building_id"] = pd.util.hash_pandas_object(meters["Building"])
meters = meters.rename(columns={"Id":"meter_id", "Name":"unit", "Entity":"meter_name", "Room":"room", "Floor":"floor"}).drop(columns = ["SiteName", "SiteId","DataType", "Filter_Name", "Filter_Id", "Building"])
meters = meters[~meters["meter_name"].str.contains("KEY_PERF")]

meters.to_csv("meters.csv", index=False)
sites.to_csv("sites.csv", index=False)
buildings.to_csv("buildings.csv", index=False)
