"""
This file creates a predictive model of demand given the following:

- The meter
- The Day of the Week (M - F)
- The Time of day (0 - 95)
- The Time of year (0 - 96*365-1)
- Academic Status Indicator (School Day, Weekend, Summer School)
- Temperature
- Wind Speed
"""
import pandas as pd
import numpy as np
import pickle

with open("data.pkl", "rb") as file:
    df = pickle.load(file)


df["hod"] = 1 + 4*df["datetime"].dt.hour + df["datetime"].dt.minute / 15
df["hoy"] = 96*df["datetime"].dt.dayofyear + df["hod"]
df["dow"] = df["datetime"].dt.dayofweek

df.to_csv("data.csv")
