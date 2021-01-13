import numpy as np
from flask import json
from numpy import unicode

from DBConnection import Db
from segmentation import *
from coding import *
import os


def compare_codes(a, b, mask_a, mask_b, rotation=False):
    """Compares two codes and calculates Jaccard index.

    :param a: Code of the first iris
    :param b: Code of the second iris
    :param mask_a: Mask of the first iris
    :param mask_b: Mask of the second iris
    :param rotation: Maximum cyclic rotation of the code. If this argument is greater than zero, the function will
        return minimal distance of all code rotations. If this argument is False, no rotations are calculated.

    :return: Distance between two codes.
    """
    if rotation:
        d = []
        for i in range(-rotation, rotation + 1):
            c = np.roll(b, i, axis=1)
            mask_c = np.roll(mask_b, i, axis=1)
            d.append(np.sum(np.remainder(a + c, 2) * mask_a * mask_c) / np.sum(mask_a * mask_c))
        return np.min(d)
    return np.sum(np.remainder(a + b, 2) * mask_a * mask_b) / np.sum(mask_a * mask_b)


def encode_photo(image):
    """Finds the pupil and iris of the eye, and then encodes the unravelled iris.

    :param image: Image of an eye
    :return: Encoded iris (code, mask)
    :rtype: tuple (ndarray, ndarray)
    """
    img = preprocess(image)
    x, y, r = find_pupil_hough(img)
    x_iris, y_iris, r_iris = find_iris_id(img, x, y, r)
    iris = unravel_iris(image, x, y, r, x_iris, y_iris, r_iris)
    return iris_encode(iris)


def save_codes(data):
    """Takes data, and saves encoded images to 'codes' directory.

    :param data: Data formatted as returned by load_* functions from datasets.py module (dictionary with keys 'data' and
        'target')
    :type data: dict
    """
    for i in range(len(data['data'])):
        print("{}/{}".format(i, len(data['data'])))
        image = cv2.imread(data['data'][i])
        try:
            code, mask = encode_photo(image)
            np.save('codes\\code{}'.format(i), np.array(code))
            np.save('codes\\mask{}'.format(i), np.array(mask))
            np.save('codes\\target{}'.format(i), data['target'][i])
        except:
            np.save('codes\\code{}'.format(i), np.zeros(1))
            np.save('codes\\mask{}'.format(i), np.zeros(1))
            np.save('codes\\target{}'.format(i), data['target'][i])


def load_codes():
    """Loads codes saved by save_codes function.

    :return: Codes, masks, and targets of saved images
    :rtype: tuple (ndarray, ndarray, ndarray)
    """
    codes = []
    masks = []
    targets = []
    i = 0
    while os.path.isfile('codes\\code{}.npy'.format(i)):
        code = np.load('codes\\code{}.npy'.format(i))
        if code.shape[0] != 1:
            codes.append(code)
            masks.append(np.load('codes\\mask{}.npy'.format(i)))
            targets.append(np.load('codes\\target{}.npy'.format(i)))
        i += 1
    return np.array(codes), np.array(masks), np.array(targets)


def split_codes(codes, masks, targets):
    """Splits data for testing purposes.

    The first piece of data (code, mask, target) for each target is separated from the rest.

    :param codes: Array of codes
    :param masks: Array of masks
    :param targets: Array of targets
    :return: All codes, masks, and targets without the first instance of each target, then codes, masks, and targets of
        containing test examples
    :rtype: 6-tuple of ndarrays
    """
    X_test = []
    X_base = []
    M_test = []
    M_base = []
    y_test = []
    y_base = []
    for i in range(targets.max() + 1):
        X = codes[targets == i]
        M = masks[targets == i]
        X_test.append(X[0])
        X_base.append(X[1:])
        M_test.append(M[0])
        M_base.append(M[1:])
        y_test.append(i)
        y_base += [i] * X[1:].shape[0]
    return np.vstack(X_base), np.vstack(M_base), np.array(y_base), np.array(X_test), np.array(M_test), np.array(y_test)


if __name__ == '__main__':
    data = load_utiris()['data']
    # image = cv2.imread(data[0])
    # image2 = cv2.imread(data[6])


    # ===========================================================================

    img = cv2.imread("S2005R07.jpg", 0)
    img = cv2.medianBlur(img, 5)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, img.shape[0] / 64, param1=200, param2=30,
                               minRadius=10, maxRadius=0)
    circles = np.uint16(np.around(circles))
    crop_img = None
    for i in circles[0, :]:
        x = 100
        # crop_img = cimg[i[1] - i[2] - x:i[1] + i[2] + x, i[0] - i[2] - x:i[0] + i[2] + x]
        # crop_img = cimg[i[1] - 3 * i[2]:i[1] + 3 * i[2] , i[0] - i[2] - 4 * i[2]:i[0] + 4 * i[2]]
        crop_img = cimg[i[1] - 3 * i[2]:i[1] + 3 * i[2] , i[0] - 3 * i[2] :i[0] +  3 * i[2]]

    crop_img = cv2.resize(crop_img, (256, 256))
    if crop_img is not None:
        cv2.imwrite('sb.jpg', crop_img)
    else:
        cv2.imwrite('sb.jpg', cimg)
    # ===========================================================================================
    img1 = cv2.imread("S2005R09.jpg", 0)
    img1 = cv2.medianBlur(img1, 5)
    cimg1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)

    circles1 = cv2.HoughCircles(img1, cv2.HOUGH_GRADIENT, 1, img1.shape[0] / 64, param1=200, param2=30,
                               minRadius=10, maxRadius=0)
    circles1 = np.uint16(np.around(circles1))
    crop_img1 = None
    for i in circles1[0, :]:
        x = 100
        # crop_img1 = cimg1[i[1] - i[2] - x:i[1] + i[2] + x, i[0] - i[2] - x:i[0] + i[2] + x]
        crop_img1 = cimg1[i[1] - 3 * i[2]:i[1] + 3 * i[2], i[0] - 3 * i[2]:i[0] + 3 * i[2]]
        # crop_img1 = cimg1[i[1] - i[2]:i[1] + i[2] , i[0] - i[2] :i[0] +  i[2]]

    crop_img1 = cv2.resize(crop_img1, (256, 256))
    if crop_img1 is not None:
        cv2.imwrite('sb2.jpg', crop_img1)
    else:
        cv2.imwrite('sb2.jpg', cimg1)
    # ===========================================================================================

    image = cv2.imread("S2005R07.jpg")
    image2 = cv2.imread("S2005R07.jpg")

    image = cv2.resize(image, (256, 256))
    image2 = cv2.resize(image2, (256, 256))
    # image = cv2.imread("sb.jpg")
    # image2 = cv2.imread("sb2.jpg")

    print(image.shape)
    print(image2.shape)
    code, mask = encode_photo(image)
    code2, mask2 = encode_photo(image2)

    print(compare_codes(code, code2, mask, mask2))
    print("------------------------------------------------------")
# ===============================================================
    np.savetxt("test.txt", code)

    import base64

    db = Db()
    with open("test.txt", "rb") as imageFile:
        st = str(base64.b64encode(imageFile.read()))
        print(st)
        z=st[1:]
        print(z)
        e = "insert into sample values(" +z + ")"
        print(e)
        id1 = db.insert(e)

    s=db.selectOne("select * from sample")
    x=s['tt']
    str2 = bytes(x, encoding="UTF-8")

    zz=base64.b64decode(str2)

    fh = open("imageToSave.txt", "wb")
    fh.write(zz)
    fh.close()

    y = np.loadtxt("imageToSave.txt")
    print(y)


    np.savetxt("test2.txt", code2)
    y2 = np.loadtxt("test2.txt")
    print(y2)

    print(compare_codes(y, y2, mask, mask2))
# ===============================================================
    shape=code.shape
    shape2=code2.shape
    print(str(shape[0])+"----"+str(shape[1]))
    print(str(shape2[0])+"----"+str(shape2[1]))

    import base64
    import numpy as np

    # t = code2
    # s = base64.b64encode(t)
    # r = base64.decodebytes(s)
    # q = np.frombuffer(r, dtype=np.float64)
    #
    # print(np.allclose(q, t))

    # lists = code2.tolist()
    # db = Db()
    # b = "insert into sample values('" +str(lists) + "')"
    # id1 = db.insert(b)
    #
    # sss=db.selectOne("select * from sample")
    # a=sss['tt']
    #
    # xxxx=np.array(a).tolist()
    # print(compare_codes(code, xxxx, mask, mask2))



    # # js=json.dumps(lists)
    # print("jjj---------" + str(lists))
    # cc=u', '.join([unicode(x.decode('utf-8')) if type(x) == type(str()) else unicode(x) for x in lists])
    #
    # res = cc.split('], [')
    # cd2 = np.array(res)
    #
    # shape2=cd2.shape
    # print(str(shape2[0])+"---==-")

    # s = code2.tostring()
    # print("Binary string array:")
    # print(s)
    # print("Array using fromstring():")
    # y = np.fromstring(s)
    # print(y)
    # # print("The decoded ",x)
    # xx=np.ndarray(y)
