import pandas as pd
import numpy as np
import json
import os
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


kw = pd.DataFrame(columns=['SiteId', 'SiteName', 'TagId', 'SiteDateTime', 'DateTimeUtc', 'Mean',
                           'Min', 'Max', 'Median', 'Sample', 'StDev', 'SampleSize',
                           'ActualSampleSize', 'Quality', 'MinTsUtc', 'MaxTsUtc', 'SampleTsUtc'])
kwh = pd.DataFrame(columns=['SiteId', 'SiteName', 'TagId', 'SiteDateTime', 'DateTimeUtc', 'Mean',
                            'Min', 'Max', 'Median', 'Sample', 'StDev', 'SampleSize',
                            'ActualSampleSize', 'Quality', 'MinTsUtc', 'MaxTsUtc', 'SampleTsUtc'])

kw['SiteDateTime'] = pd.to_datetime(kw["SiteDateTime"])
kw['DateTimeUtc'] = pd.to_datetime(kw["DateTimeUtc"])
kw['MinTsUtc'] = pd.to_datetime(kw["MinTsUtc"])
kw['MaxTsUtc'] = pd.to_datetime(kw["MinTsUtc"])
kw['SampleTsUtc'] = pd.to_datetime(kw["SampleTsUtc"])
kw['Mean'] = kw['Mean'].astype(np.float64)
kw['Max'] = kw['Max'].astype(np.float64)
kw['Min'] = kw['Min'].astype(np.float64)
kw['Median'] = kw['Median'].astype(np.float64)
kw['Sample'] = kw['Sample'].astype(np.int32)
kw['StDev'] = kw['StDev'].astype(np.float64)
kw['SampleSize'] = kw['SampleSize'].astype(np.int32)
kw['ActualSampleSize'] = kw['ActualSampleSize'].astype(np.int32)
kw['Quality'] = kw['Quality'].astype(np.bool)

kwh['SiteDateTime'] = pd.to_datetime(kwh["SiteDateTime"])
kwh['DateTimeUtc'] = pd.to_datetime(kwh["DateTimeUtc"])
kwh['MinTsUtc'] = pd.to_datetime(kwh["MinTsUtc"])
kwh['MaxTsUtc'] = pd.to_datetime(kwh["MinTsUtc"])
kwh['SampleTsUtc'] = pd.to_datetime(kwh["SampleTsUtc"])
kwh['Mean'] = kwh['Mean'].astype(np.float64)
kwh['Max'] = kwh['Max'].astype(np.float64)
kwh['Min'] = kwh['Min'].astype(np.float64)
kwh['Median'] = kwh['Median'].astype(np.float64)
kwh['Sample'] = kwh['Sample'].astype(np.int32)
kwh['StDev'] = kwh['StDev'].astype(np.float64)
kwh['SampleSize'] = kwh['SampleSize'].astype(np.int32)
kwh['ActualSampleSize'] = kwh['ActualSampleSize'].astype(np.int32)
kwh['Quality'] = kwh['Quality'].astype(np.bool)

user, password, postgres_address, ssh_address = os.popen('pass show postgres').read().split()
server = SSHTunnelForwarder(
    (ssh_address.split(':')[0], int(ssh_address.split(':')[1])),
    ssh_username=user,
    ssh_password=password,
    ssh_pkey='~/.ssh/id_rsa',
    ssh_private_key_password=password,
    remote_bind_address=('127.0.0.1', int(postgres_address.split(':')[1])))

with server as tunnel:
    engine = create_engine(f'postgresql://{user}:{password}@127.0.0.1:{str(server.local_bind_port)}/uhm2023')
    session = sessionmaker(bind=engine)()
    kw.to_sql("kw", con=engine, schema="aurora_api", if_exists="replace", index=False)
    kwh.to_sql("kwh", con=engine, schema="aurora_api", if_exists="replace", index=False)

    data_path = "../data/aurora/"
    for filename in os.listdir(data_path):
        if filename == "filter.json":
            print("Creating Metadata")
            with open(data_path + filename, "rb") as filter_file:
                meters = pd.json_normalize(json.load(filter_file),
                                           record_path=["Tags"],
                                           meta=["Id", "Name"],
                                           meta_prefix = "Filter_")
                
                meters = meters[~meters["Building"].isna()]
                sites = meters.groupby("SiteName").first().drop(columns=["Building", "Floor", "Room", "DataType", "Filter_Id", "Filter_Name", "Entity", "Name", "Id"])
                buildings = meters.groupby("Building").first().drop(columns=["Filter_Name", "Filter_Id", "DataType", "Room", "Floor", "SiteName", "Entity", "Name", "Id"])

                buildings = buildings.reset_index().rename(columns={"Building":"building_name", "SiteId":"site_id"})
                buildings["building_id"] = pd.util.hash_pandas_object(buildings["building_name"]).astype(np.int32)
                meters["building_id"] = pd.util.hash_pandas_object(meters["Building"]).astype(np.int32)

                meters.to_sql("meters", con=engine, schema="aurora_api", if_exists="replace",index=False)
                sites.to_sql("sites", con=engine, schema="aurora_api", if_exists="replace",index=False)
                buildings.to_sql("buildings", con=engine, schema="aurora_api", if_exists="replace",index=False)
            continue
        with open(data_path + filename, "rb") as datafile:
            data = pd.json_normalize(json.load(datafile))
            data['SiteDateTime'] = pd.to_datetime(data["SiteDateTime"])
            data['DateTimeUtc'] = pd.to_datetime(data["DateTimeUtc"])
            data['MinTsUtc'] = pd.to_datetime(data["MinTsUtc"])
            data['MaxTsUtc'] = pd.to_datetime(data["MinTsUtc"])
            data['SampleTsUtc'] = pd.to_datetime(data["SampleTsUtc"])
            if "kw" in filename and "kwh" not in filename:
                print("Appending kw using:", filename)
                data.to_sql("kw", con=engine, schema="aurora_api", if_exists="append",index=False)
            if "kwh" in filename:
                 print("Appending kwh using:", filename)
                 data.to_sql("kwh", con=engine, schema="aurora_api", if_exists="append", index = False)


"""
Using the Login information as before, tunnel into the server using SSH.
Create the PostgreSQL engine, and construct a session.
"""

