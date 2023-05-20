import tensorflow as tf

from load_dataset import load_github_data_dataset, load_github_data_array

from neural_networks.nn_one_layer import build_and_compile_one_layer_model
from neural_networks.nn_6_layer import build_and_compile_six_layer_model
from neural_networks.randomforest import build_and_compile_rf_model

def main():
    train_ds, test_ds = load_github_data_dataset()
    # X_train, X_test, y_train, y_test = load_github_data_array()
    
    num_features = 17
    
    # Replace with a real strategy for distributed training
    strategy = tf.distribute.get_strategy()
    
    with strategy.scope():
        random_forest_model = build_and_compile_rf_model()
        one_layer_model = build_and_compile_one_layer_model(num_features)
        six_layer_model = build_and_compile_six_layer_model(num_features)
    
    random_forest_model.fit(train_ds)
    one_layer_model.fit(train_ds, epochs=500, batch_size=4)
    six_layer_model.fit(train_ds, epochs=500, batch_size=4)
    
    models = [one_layer_model, six_layer_model, random_forest_model]
    
    best_score = -float("Inf")
    best_model = None
    
    for model in models:
        evaluation = model.evaluate(test_ds)
        score = evaluation[1]
        
        if score > best_score:
            best_score = score
            best_model = model
            
    print("Best model: ", best_model)
    print("Best score: ", best_score)
    print("Saving model...")
    best_model.save("model", save_format="tf")

if __name__ == '__main__':
    main()