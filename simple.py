import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pytesseract as pyt
import labels
import distort
from distort import warp_cylindrical
import cv2
from PIL import Image

def create_model():
    # TODO: Add critic model as well, double up! https://keras.io/examples/rl/actor_critic_cartpole/
    inputs = keras.Input(shape=(1024, 1024, 4))
    layer1 = layers.Conv2D(32, 8, strides=4, activation="relu")(inputs)
    layer2 = layers.Conv2D(64, 4, strides=2, activation="relu")(layer1)
    layer3 = layers.Conv2D(64, 3, strides=1, activation="relu")(layer2)

    layer4 = layers.Flatten()(layer3)

    layer5 = layers.Dense(512, activation="relu")(layer4)
    transformation = layers.Dense(15, activation="linear")(layer5)

    return keras.Model(inputs=inputs, outputs=transformation)


model = create_model()

optimizer = keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)
huber_loss = keras.losses.Huber()

rewards_history = []
running_reward = 0.0

for i in range(100):
    id, img, label = labels.generate_label()
    distorted = distort.distort(np.array(img))
    transformation = model(distorted)
    affine = np.reshape(transformation[:6], (2, 3))
    cylindrical = np.reshape(transformation[6:], (3, 3))
    decylindered = warp_cylindrical(distorted, cylindrical)
    dewarped = cv2.warpAffine(decylindered, affine, (1024, 1024))
    img2 = Image.fromarray(dewarped)
    result = pyt.image_to_string(img2, lang="dan")

    # TODO: Compute some kind of integrity score for the outputted string
    
