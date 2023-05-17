import tensorflow as tf
import os
import json

os.environ["GRPC_FAIL_FAST"] = "use_caller"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

os.environ["TF_CONFIG"] = json.dumps({
    "cluster": {
        "worker": ["localhost:8870"],
        "ps": ["localhost:8880"]
    },
    "task": {"type": "worker", "index": 0}
})

cluster_resolver = tf.distribute.cluster_resolver.TFConfigClusterResolver()

server = tf.distribute.Server(
    cluster_resolver.cluster_spec(),
    job_name=cluster_resolver.task_type,
    task_index=cluster_resolver.task_id,
    protocol=cluster_resolver.rpc_layer or "grpc",
    start=True)
server.join()
