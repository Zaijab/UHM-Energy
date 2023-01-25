import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from model import LSTNet

data = pd.read_csv("../data/data.csv")
y = np.log(data["kw_average"].to_numpy())

# Fit the model
model = LSTNet(
    y=y,
    forecast_period=96,
    lookback_period=96*7,
    kernel_size=3,
    filters=4,
    gru_units=4,
    skip_gru_units=3,
    skip=50,
    lags=100,
)

model.fit(
    loss='mse',
    learning_rate=0.01,
    batch_size=128,
    epochs=100,
    verbose=1)

total_predictions = model.predict(index=y.shape[0] - 96*1) 
total_day = total_predictions[~total_predictions["predicted_1"].isna()]
total_day["error"] = ((total_day["actual_1"] - total_day["predicted_1"])**2).sum()


for i in range(365):
    predictions = model.predict(index=y.shape[0] - 96*(i+2))
    day = predictions[~predictions["predicted_1"].isna()]
    day["error"] = ((day["actual_1"] - day["predicted_1"])**2).sum()
    total_day = pd.concat([day, total_day])
data_to_send = data.merge(total_day, how="left",left_index=True, right_index=True)

data_to_send["actual_1"] = np.exp(data_to_send["actual_1"])
data_to_send["predicted_1"] = np.exp(data_to_send["predicted_1"])

data_to_send[~data_to_send["error"].isna()].to_csv("predictions.csv", index=False)
