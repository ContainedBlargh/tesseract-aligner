# Somehow take the labels and use them as textures for cylinders, boxes and such
# Then, take a picture.

from pythreejs import *
from IPython.display import display
from math import pi

from pythreejs._example_helper import use_example_model_ids
use_example_model_ids()

from labels import generate_label

id, path, label = generate_label()
label_tex = ImageTexture(imageUri=path)

label_tex
