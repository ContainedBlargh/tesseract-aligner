import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pytesseract as pyt
import labels
import distort

inputs = keras.Input(shape=(1024, 1024, 4))
dense = layers.Dense(64, activation="relu")
y = dense(inputs)

pyt.image_to_string()
