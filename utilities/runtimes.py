import pandas as pd

file = "view_frog2_hvac_power_5min.csv"

def get_session_statistics(df):
    energy_usage = ((df["datetime"].max() - df["datetime"].min()).total_seconds() / 3600) * df["Power Avg (kW)"].mean()
    interval_hours = (df["datetime"].max() - df["datetime"].min()).total_seconds() / 3600
    new_dataframe = df.head(1)
    
    new_dataframe["Power Avg (kW)"] = df["Power Avg (kW)"].mean()
    new_dataframe["Energy Usage (kWh)"] = energy_usage
    new_dataframe["interval_hours"] = interval_hours
    return new_dataframe

ac_data = pd.read_csv(f"data/frogs/{file}")

ac_data["datetime"] = pd.to_datetime(ac_data["datetime"])
starters = (ac_data[ac_data["Power Avg (kW)"] > 0.05]["datetime"].diff() != "00:05:00")
starters = ac_data[ac_data.join(starters, rsuffix="_delta")["datetime_delta"] == True]
starters["type_s"] = "start"
enders = (ac_data[ac_data["Power Avg (kW)"] > 0.05]["datetime"].diff(-1) != "-00:05:00")
finishers = ac_data[ac_data.join(enders, rsuffix="_delta")["datetime_delta"] == True]
finishers["type_e"] = "end"
big = pd.concat([ac_data, starters[["type_s"]], finishers[["type_e"]]], axis=1).reindex(ac_data.index)
big = big[big["Power Avg (kW)"] > 0.05]
big["type"] = big["type_s"].fillna("") + big["type_e"].fillna("")
big.loc[big["type"]=="start", "session"] = big.index[big["type"] == "start"]
big["session"] = big["session"].fillna(method='ffill').astype(int)
result = big.groupby("session").apply(get_session_statistics).drop(columns=["type_s", "type_e", "type", "session"])

result.to_csv(f"data/frogs_upload/{file}", index=False)
