from hashlib import new
import numpy as np
import cv2
from random import uniform
import os


def pad_image(img, size: int):
    old_size = img.shape[:2]
    ratio = float(size)/max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    im2 = cv2.resize(img, (new_size[1], new_size[0]))
    delta_w = size - new_size[1]
    delta_h = size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)
    color = [0, 0, 0, 0]
    im3 = cv2.copyMakeBorder(im2, top, bottom, left,
                             right, cv2.BORDER_CONSTANT, value=color)
    return im3


def warp_cylindrical(img, K=None):
    # STOLEN FROM A GIST: https://gist.github.com/royshil/0b21e8e7c6c1f46a16db66c384742b2b
    h_, w_ = img.shape[:2]
    if K is None:
        K = np.array([[800, 0,   w_/2],
                      [0,   800, h_/2],
                      [0,   0,   1]])
    """This function returns the cylindrical warp for a given image and intrinsics matrix K"""
    # pixel coordinates
    y_i, x_i = np.indices((h_, w_))
    X = np.stack([x_i, y_i, np.ones_like(x_i)],
                 axis=-1).reshape(h_*w_, 3)  # to homog
    Kinv = np.linalg.inv(K)
    X = Kinv.dot(X.T).T  # normalized coords
    # calculate cylindrical coords (sin\theta, h, cos\theta)
    A = np.stack([np.sin(X[:, 0]), X[:, 1], np.cos(X[:, 0])],
                 axis=-1).reshape(w_*h_, 3)
    B = K.dot(A.T).T  # project back to image-pixels plane
    # back from homog coords
    B = B[:, :-1] / B[:, [-1]]
    # make sure warp coords only within image bounds
    B[(B[:, 0] < 0) | (B[:, 0] >= w_) | (B[:, 1] < 0) | (B[:, 1] >= h_)] = -1
    B = B.reshape(h_, w_, -1)

    # for transparent borders...
    #img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    # warp the image according to cylindrical coords
    return cv2.remap(img, B[:, :, 0].astype(np.float32), B[:, :, 1].astype(np.float32), cv2.INTER_CUBIC)


def distort(img):
    img = pad_image(img, 1024)
    h, w = img.shape[:2]
    cv2. waitKey(0)
    w_c = np.float32([[uniform(w / 3, h), 0, w / 2],
                      [0, uniform(h / 3, w), h / 2],
                      [0, 0, 1]])

    w_a = np.float32([[uniform(0.5, 1), 0,               0],
                      [0,               uniform(0.5, 1), uniform(-h/5, h/5)]])
    w_r = cv2.getRotationMatrix2D(
        (uniform(w/4, w/2), uniform(h/4, h/2)), uniform(-45, 45), 1)
    print("w_c.shape", w_c.shape)
    print("w_r.shape", w_r.shape)
    # res = cv2.warpAffine(img, w_a, (w, h))
    rot = cv2.warpAffine(img, w_r, (w, h))
    warped = warp_cylindrical(rot, w_c)
    # TODO: Add noisy background to make the problem harder
    # This could be like random shapes with some added blur
    # I think that opencv is more than capable of drawing random lines, squares and circles
    
    return warped

if __name__ == "__main__":
    for f in os.scandir("labels"):
        id_and_extension = f.name.split("label-")[1]
        img = cv2.imread(f.path, cv2.IMREAD_UNCHANGED)
        distorted = distort(img)
        cv2.imwrite(f"distortions/distort-{id_and_extension}", distorted)
