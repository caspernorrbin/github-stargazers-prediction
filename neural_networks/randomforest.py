import tensorflow_addons as tfa
import tensorflow_decision_forests as tfdf

def build_and_compile_rf_model():
    model = tfdf.keras.RandomForestModel(task=tfdf.keras.Task.REGRESSION)
    model.compile(metrics=[tfa.metrics.RSquare()])
    return model