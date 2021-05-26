import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from resolution import X, Y
from uuid import uuid4 as uuid
from random import randint, uniform
from pytesseract import image_to_string
from PIL import Image
from os import remove

fonts = [
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\DejaVuSerif-BoldItalic.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\DejaVuSerif-Bold.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\STIXGeneralBolIta.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\DejaVuSerif.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\DejaVuSansMono.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\STIXGeneralBol.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\DejaVuSans-Bold.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\DejaVuSansMono-Bold.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\DejaVuSans-BoldOblique.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\DejaVuSansMono-BoldOblique.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\STIXGeneral.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\DejaVuSansMono-Oblique.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\STIXGeneralItalic.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\DejaVuSans.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\DejaVuSans-Oblique.ttf",
    "C:\\Users\\jovtottrup\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\matplotlib\\mpl-data\\fonts\\ttf\\DejaVuSerif-Italic.ttf",
    "C:\\WINDOWS\\Fonts\\ARLRDBD.TTF",
    "C:\\Windows\\Fonts\\BRLNSB.TTF",
    "C:\\Windows\\Fonts\\GLSNECB.TTF",
    "C:\\WINDOWS\\Fonts\\LFAXD.TTF",
    "C:\\Windows\\Fonts\\calibril.ttf"
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
        amount_to_replace = randint(int(uniform(0, len(spaces) - 1)), len(spaces) - 1)
        for i in range(amount_to_replace):
            p = randint(0, len(spaces) - 1)
            exploded[spaces[p]] = "\n"
        label = "".join(exploded)
        id = uuid()
        fprop = FontProperties()
        fprop.set_file(fonts[randint(0, len(fonts) - 1)])
        fprop.set_size(32)
        path = f'labels/label-{id}.png' 
        plt.text(0, 0.5, label, fontproperties=fprop)
        plt.axis('off')
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        test = "\n".join(image_to_string(Image.open(path), lang="dan").splitlines()[:-1])
        if label.strip() != test.strip():
            remove(path)
            continue
        return id, path, label

if __name__ == "__main__":
    for i in range(4):
        id, path, label = generate_label()
        test = "\n".join(image_to_string(Image.open(path), lang="dan").splitlines()[:-1])
        print(label)
        print(test.strip())
        print(label == test.strip())
