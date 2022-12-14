import numpy as np
from model import LSTNet

# Generate two time series
N = 1000
t = np.linspace(0, 1, N)
e = np.random.multivariate_normal(mean=np.zeros(2), cov=np.eye(2), size=N)
a = 40 + 30 * t + 20 * np.cos(2 * np.pi * (10 * t - 0.5)) + e[:, 0]
b = 50 + 40 * t + 30 * np.cos(2 * np.pi * (20 * t - 0.5)) + e[:, 1]
y = np.hstack([a.reshape(- 1, 1), b.reshape(- 1, 1)])

# Fit the model
model = LSTNet(
    y=y,
    forecast_period=100,
    lookback_period=200,
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
    batch_size=64,
    epochs=100,
    verbose=1
)

# Plot the in-sample predictions
predictions = model.predict(index=900)
fig = model.plot_predictions()
fig.write_image('predictions.png', width=750, height=650)

# Plot the out-of-sample forecasts
forecasts = model.forecast()
fig = model.plot_forecasts()
fig.write_image('forecasts.png', width=750, height=650)
