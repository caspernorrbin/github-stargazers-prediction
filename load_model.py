import tensorflow as tf
import tensorflow_decision_forests as tfdf
import tensorflow_addons as tfa

from load_dataset import load_github_data_dataset, load_github_data_array

def main():
    train_ds, test_ds = load_github_data_dataset()
    
    model = tf.keras.saving.load_model("model")
    score = model.evaluate(test_ds, return_dict=True)
    print(score)

if __name__ == '__main__':
    main()