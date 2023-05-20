import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def load_github_data_array():
    # Load dataset
    df = pd.read_csv('github/top_repos.csv')

    # Drop all entrys with nan
    df = df.dropna(axis=0)

    # Split dataset
    y = df['Stargazers']
    X = df.drop('Stargazers', axis=1)
    X = X.drop('Name', axis=1)
    
    if 'Language' in X.columns:
        category_mapping = {category: index for index, category in enumerate(
            X['Language'].unique())}
        
        X['Language'] = X['Language'].map(category_mapping)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Normalizing the data
    scaler = MinMaxScaler()
    scaler.fit(X_train)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test

def load_github_data_dataset(batch_size=4):
    X_train, X_test, y_train, y_test = load_github_data_array()
    
    train_ds = tf.data.Dataset.from_tensor_slices((X_train, y_train)).batch(batch_size)
    test_ds = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(batch_size)

    return train_ds, test_ds
