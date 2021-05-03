import tensorflow as tf
# print("Num GPUs Available: ", *tf.config.experimental.list_physical_devices())

# from tensorflow.python.client import device_lib
# print(device_lib.list_local_devices())
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())