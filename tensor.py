import tensorflow as tf

# Muestra las capacidades de la CPU para TensorFlow
print("Capacidades de la CPU para TensorFlow:", tf.config.experimental.get_visible_devices("CPU"))

# Verifica si TensorFlow utiliza instrucciones AVX
avx_supported = tf.config.experimental.list_physical_devices('CPU')[0].device_type == 'CPU'
print("AVX Soportado:", avx_supported)
