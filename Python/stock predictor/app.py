import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.api.models import Sequential
from keras.api.layers import Dense, LSTM

# Download stock data
stock_data = yf.download('AAPL', start='2010-01-01', end='2023-01-01')
print(stock_data.head())

# Use only the 'Close' price for prediction
data = stock_data['Close'].values.reshape(-1, 1)

# Normalize data to the range (0, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

training_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:training_size]
test_data = scaled_data[training_size - 60:]

# Prepare training data
def create_dataset(data, time_step=60):
    X, y = [], []
    for i in range(time_step, len(data)):
        X.append(data[i - time_step:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)

X_train, y_train = create_dataset(train_data)
X_test, y_test = create_dataset(test_data)

# Reshape input to be [samples, time steps, features]
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

model = Sequential()

# LSTM layers
model.add(LSTM(units=50, return_sequences=True, input_shape=(60, 1)))
model.add(LSTM(units=50, return_sequences=False))

# Fully connected layer
model.add(Dense(units=25))
model.add(Dense(units=1))  # Output layer (predicting next day's price)

# Compile model
model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_train, y_train, batch_size=64, epochs=10)

predictions = model.predict(X_test)

# Reverse the scaling of predictions
predictions = scaler.inverse_transform(predictions)

# Reverse the scaling of the actual test data
y_test = scaler.inverse_transform(y_test.reshape(-1, 1))

# Plot the predictions vs actual stock prices
plt.figure(figsize=(10, 6))
plt.plot(y_test, color='blue', label='Actual Stock Price')
plt.plot(predictions, color='red', label='Predicted Stock Price')
plt.title('Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

from sklearn.metrics import mean_squared_error

# Calculate the root mean squared error
rmse = np.sqrt(mean_squared_error(y_test, predictions))
print(f"Root Mean Squared Error: {rmse}")
