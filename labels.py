import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from resolution import X, Y
from uuid import uuid4 as uuid
from random import randint, uniform
from pytesseract import image_to_string
from PIL import Image
from os import remove
import io

font_families = [
    'serif', 'sans-serif', 'cursive',
    'fantasy', 'monospace'
]


class dictionary:
    def __init__(self, words) -> None:
        self.n = len(words)
        self.words = words

    def sample(self):
        p = randint(0, self.n - 1)
        return self.words[p]


def load_danish():
    fp = open("all_words.txt", "r", encoding='utf8')
    return dictionary([l.strip() for l in fp])


global danish
danish = load_danish()


def generate_label(min=6, max=18):
    """
    Generate a label, save it as a texture and return the path to the texture.
    """
    while True:
        amount = randint(min, max)
        label = " ".join([danish.sample() for _ in range(amount)])
        exploded = list(label)
        spaces = [i for i, l in enumerate(exploded) if l == " "]
        amount_to_replace = randint(
            int(uniform(0, len(spaces) - 1)), len(spaces) - 1)
        for i in range(amount_to_replace):
            p = randint(0, len(spaces) - 1)
            exploded[spaces[p]] = "\n"
        label = "".join(exploded)
        id = uuid()
        fprop = FontProperties()
        fprop.set_family(font_families[randint(0, len(font_families) - 1)])
        fprop.set_size(32)
        plt.text(0, 0.5, label, fontproperties=fprop)
        plt.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, bbox_inches='tight', transparent=True)
        plt.close()
        buf.seek(0)
        img = Image.open(buf)
        test = "\n".join(image_to_string(img, lang="dan").splitlines()[:-1])
        if label.strip() != test.strip():
            buf.close()
            del buf
            continue
        return id, img, label


if __name__ == "__main__":
    for i in range(4):
        id, img, label = generate_label()
        test = "\n".join(image_to_string(img, lang="dan").splitlines()[:-1])
        img.save(f'labels/label-{id}.png')
        print(label)
        print(test.strip())
        print(label == test.strip())
