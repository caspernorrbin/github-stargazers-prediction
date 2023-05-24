import os
import time
import pandas as pd
import ray
from ray import tune
import tensorflow as tf
import tensorflow_addons as tfa
import tensorflow_decision_forests as tfdf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


def load_dataset():
    df = pd.read_csv("top_repos.csv")
    y = df['Stargazers']
    X = df.drop('Stargazers', axis=1)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
   
    scaler = MinMaxScaler()
    scaler.fit(X_train)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    y_train = y_train.to_numpy()
    y_test = y_test.to_numpy()
    
    return X_train, X_test, y_train, y_test

def compile_rf_model():
    model = tfdf.keras.RandomForestModel(task=tfdf.keras.Task.REGRESSION)
    model.compile(metrics=[tfa.metrics.RSquare()])
    return model

def compile_one_layer_model():
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(17,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(
        loss=tf.keras.losses.MeanSquaredError(),
        optimizer=tf.keras.optimizers.Adam(),
        metrics=[tfa.metrics.RSquare()])    
    return model

def compile_six_layer_model():
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(17,)),
        tf.keras.layers.Dense(18, activation='relu'),
        tf.keras.layers.Dense(36, activation='relu'),
        tf.keras.layers.Dense(72, activation='relu'),
        tf.keras.layers.Dense(144, activation='relu'),
        tf.keras.layers.Dense(72, activation='relu'),
        tf.keras.layers.Dense(36, activation='relu'),
        tf.keras.layers.Dense(18, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(
        loss=tf.keras.losses.MeanSquaredError(),
        optimizer=tf.keras.optimizers.Adam(),
        metrics=[tfa.metrics.RSquare()])    
    return model

def compile_nn_model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(64, activation='relu', input_shape=(17,)))
    model.add(tf.keras.layers.Dense(32, activation='relu'))
    model.add(tf.keras.layers.Dense(1))

    model.compile(
        loss=tf.keras.losses.MeanSquaredError(),
        optimizer=tf.keras.optimizers.Adam(),
        metrics=[tfa.metrics.RSquare()])    
    return model

def train_rf_model():
    X_train, X_test, y_train, y_test = load_dataset()   
    model = compile_rf_model()  

    model.fit(X_train, y_train, verbose=0)
    
    loss, score = model.evaluate(X_test, y_test)
    
    return model, score

def train_one_layer_model(config):
    X_train, X_test, y_train, y_test = load_dataset()   
    model = compile_one_layer_model()  

    model.fit(
        X_train,
        y_train,
        batch_size=config["batch_size"],
        epochs=config["epochs"],
        verbose=0
    )
    loss, score = model.evaluate(X_test, y_test)
    
    with tune.checkpoint_dir(step=0) as checkpoint_dir:
        model.save(checkpoint_dir)
    
    return {"score": score}
    
def train_six_layer_model(config):
    X_train, X_test, y_train, y_test = load_dataset()   
    model = compile_six_layer_model()  

    model.fit(
        X_train,
        y_train,
        batch_size=config["batch_size"],
        epochs=config["epochs"],
        verbose=0
    )
    loss, score = model.evaluate(X_test, y_test)
    
    with tune.checkpoint_dir(step=0) as checkpoint_dir:
        model.save(checkpoint_dir)
    
    return {"score": score}

def train_nn_model(config):
    X_train, X_test, y_train, y_test = load_dataset()   
    model = compile_nn_model()  

    model.fit(
        X_train,
        y_train,
        batch_size=config["batch_size"],
        epochs=config["epochs"],
        verbose=0
    )
    loss, score = model.evaluate(X_test, y_test)
    
    with tune.checkpoint_dir(step=0) as checkpoint_dir:
        model.save(checkpoint_dir)
    
    return {"score": score}

def main():
    os.environ["RAY_memory_usage_threshold"] = "1"
    os.environ["RAY_memory_monitor_refresh_ms"] = "0"
    ray.init()
    
    start_time = time.time()
    model, rf_score = train_rf_model()
    print("RF score: ", rf_score)

    start_tune_time = time.time()
    one_layer_tuner = tune.Tuner(
        train_one_layer_model,
        param_space={
            "batch_size": tune.grid_search([32, 64, 128]),
            "epochs": tune.grid_search([50, 100, 200, 500])
        }
    )

    results = one_layer_tuner.fit()
    best_result = results.get_best_result(metric="score", mode="max")
    one_layer_score = best_result.metrics["score"]
    print("One layer score: ", one_layer_score)
    if one_layer_score > rf_score:
        model = tf.keras.models.load_model(best_result.best_checkpoints[0][0].to_directory())
    
    
    six_layer_tuner = tune.Tuner(
        train_six_layer_model,
        param_space={
            "batch_size": tune.grid_search([32, 64, 128]),
            "epochs": tune.grid_search([50, 100, 200, 500])
        }
    )   
    
    results = six_layer_tuner.fit()
    best_result = results.get_best_result(metric="score", mode="max")
    six_layer_score = best_result.metrics["score"]
    print("Six layer score: ", six_layer_score)
    if six_layer_score > one_layer_score:
        model = tf.keras.models.load_model(best_result.best_checkpoints[0][0].to_directory())
        
        
    nn_tuner = tune.Tuner(
        train_nn_model,
        param_space={
            "batch_size": tune.grid_search([32, 64, 128]),
            "epochs": tune.grid_search([50, 100, 200, 500])
        }
    )
    
    results = nn_tuner.fit()
    best_result = results.get_best_result(metric="score", mode="max")
    nn_score = best_result.metrics["score"]
    print("NN score: ", nn_score)
    if nn_score > six_layer_score:
        model = tf.keras.models.load_model(best_result.best_checkpoints[0][0].to_directory())
    
    end_time = time.time()
    print("Total time: ", end_time - start_time)
    print("Tune time: ", end_time - start_tune_time)
    
    model.summary()
    model.save("model", save_format="tf")

if __name__ == '__main__':
    main()
    