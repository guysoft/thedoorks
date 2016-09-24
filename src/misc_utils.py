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

def cv_resize(img, scale_ratio):
    return cv2.resize(img, None,fx=scale_ratio, fy=scale_ratio, interpolation = cv2.INTER_LINEAR) # used to be cv2.INTER_CUBIC


def make_grey(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return gray

def is_not_boring_image(gray):
    hessian_threshold  = 1
    KP_MIN = 2
    KP_MAX = 15
    surf = cv2.BRISK_create(1)
    kp, des = surf.detectAndCompute(gray, None)
    if len(kp) > 3:
        print(len(kp))
    return len(kp) > KP_MIN and len(kp) < KP_MAX

