import multiprocessing
import os
import random
import tensorflow as tf
import json
import mnist_setup
import time

os.environ["TF_CONFIG"] = json.dumps({
    "cluster": {
        "worker": ["localhost:8870"],
        "ps": ["localhost:8880"],
        "chief": ["localhost:8890"]},
    "task": {"type": "chief", "index": 0}
})

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Set the environment variable to allow reporting worker and ps failure to the
# coordinator. This is a workaround and won't be necessary in the future.
os.environ["GRPC_FAIL_FAST"] = "use_caller"

cluster_resolver = tf.distribute.cluster_resolver.TFConfigClusterResolver()

strategy = tf.distribute.ParameterServerStrategy(
    cluster_resolver)

global_batch_size = 2

x = tf.random.uniform((10, 10))
y = tf.random.uniform((10,))

dataset = mnist_setup.mnist_dataset(global_batch_size)

with strategy.scope():
    model = mnist_setup.build_and_compile_cnn_model()

time_start = time.time()
model.fit(dataset, epochs=5, steps_per_epoch=20, batch_size=1)
print("Time taken: ", time.time() - time_start)

print("Evaluating")
print(model.evaluate(dataset, steps=1, batch_size=1))
