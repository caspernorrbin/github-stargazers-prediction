import os
import json

import tensorflow as tf
import mnist_setup

per_worker_batch_size = 64
os.environ["TF_CONFIG"] = json.dumps({
    "cluster": {
        "worker": ["localhost:8855", "192.168.2.2:8855"]
    },
    "task": {"type": "worker", "index": 0}
})


tf_config = json.loads(os.environ['TF_CONFIG'])
num_workers = len(tf_config['cluster']['worker'])
print("num_workers: ", num_workers)

strategy = tf.distribute.MultiWorkerMirroredStrategy()

print('Number of devices: {}'.format(strategy.num_replicas_in_sync))
global_batch_size = per_worker_batch_size * num_workers
multi_worker_dataset = mnist_setup.mnist_dataset(global_batch_size)

with strategy.scope():
  # Model building/compiling need to be within `strategy.scope()`.
  multi_worker_model = mnist_setup.build_and_compile_cnn_model()


multi_worker_model.fit(multi_worker_dataset, epochs=3, steps_per_epoch=70)