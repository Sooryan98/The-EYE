import cv2
from cv2 import IMREAD_COLOR, IMREAD_UNCHANGED
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

blarray = []
from scipy.ndimage import variance
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import laplace
from skimage.transform import resize


def variance_of_laplacian(img2):

    try:
        gray = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
    except AssertionError:
        pass
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def BGR2RGB(BGR_img):

    rgb_image = cv2.cvtColor(BGR_img, cv2.COLOR_BGR2RGB)
    return rgb_image


def blurrinesDetection(directories, threshold):
    columns = 3
    rows = len(directories) // 2
    fig = plt.figure(figsize=(5 * columns, 4 * rows))
    for i, file in enumerate(directories):
        fig.add_subplot(rows, columns, i + 1)
        img = cv2.imread(file)
        text = "Not Blurry"

        fm = variance_of_laplacian(img)
        # print(fm)
        if fm<threshold:
            blarray.append(i)

        if fm < threshold:
            text = "Blurry"
        rgb_img = BGR2RGB(img)

        cv2.putText(rgb_img, "{} : {}: {:.2f}".format(str(i),text, fm), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        plt.imshow(rgb_img)
    plt.show()
    # print(blarray)
    return blarray
