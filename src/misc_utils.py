"""
Useful functoins you can use
"""
import cv2


def cv_crop(img, x, y , h, w):
    """
    crop a opencv matrix

    :param img: the image
    :param x:
    :param y:
    :param h:
    :param w:
    :return:
    """
    #Note x and y are revesed in opencv
    return img[y:y+h, x:x+w]


def make_grey(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return gray


