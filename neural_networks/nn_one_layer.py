# Neural Network using 1 layer
# Uses 6 features for now
# R2 score of ~0.25

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import r2_score



# LOAD DATA AND PROPROCESSING
df = pd.read_csv('top_repos.csv')

# Drop all entrys with nan
df = df.dropna(axis=0)

# Split dataset
y = df['Stargazers']
X = df.drop('Stargazers', axis=1)
X = X.drop('Name', axis=1)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)




# NORMALIZING THE DATA
scaler = MinMaxScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)



# MODEL CREATION

def r2_metric(y_true, y_pred):
    return r2_score(y_true, y_pred)

model = Sequential()
model.add(Dense(32, activation='relu', input_shape=(9,)))
model.add(Dense(1))

# compile model
model.compile(loss='mean_squared_error', optimizer='adam')

# Training
model.fit(X_train, y_train, epochs=500, batch_size=4)

# Evaluation
y_pred = model.predict(X_test)
r2 = r2_metric(y_test, y_pred)
print("R2 Score:", r2)