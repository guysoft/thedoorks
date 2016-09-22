"""
Useful functoins you can use
"""


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