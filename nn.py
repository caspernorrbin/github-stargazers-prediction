import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense




# Load the dataset
data = pd.read_csv("top_repos.csv") 

# Extract features and target variable
X = data[["Forks", "Watchers", "Contributors", "Commits", "Branches", "Open PRs", "Closed PRs"]]
y = data["Stargazers"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features using MinMaxScaler
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)






model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(7,)))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')





# Train the model
history = model.fit(X_train_scaled, y_train, batch_size=32, epochs=100, validation_split=0.2)


# Evaluate the model
loss = model.evaluate(X_test_scaled, y_test)
print("Mean Squared Error on Test Set:", loss)





"""
# Make predictions
new_data = np.array([[2794, 164, 360, 2155, 5, 90, 937]])  # Replace with your own data
new_data_scaled = scaler.transform(new_data)
predictions = model.predict(new_data_scaled)
print("Predicted Stargazers:", predictions)
"""