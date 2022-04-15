import cv2
import numpy as np
from urllib.request import Request, urlopen
from pyzbar.pyzbar import decode


def url_to_image(url, read_flag=cv2.IMREAD_COLOR):
    req = Request(str(url), headers={'User-Agent': 'Mozilla/5.0'})
    resp = urlopen(req)
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, read_flag)

    # over the top shit
    # Grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Normalizing
    th, img = cv2.threshold(img, img.max()/2, 255, cv2.THRESH_OTSU)

    # Blur
    img = cv2.blur(img, (5, 5))
    # Sharpening
    
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    img = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)

    th, img = cv2.threshold(img, img.max() / 2, 255, cv2.THRESH_OTSU)
    cv2.imwrite("random.jpg", img)
    return img


def decode_qr(url):
    image = url_to_image(url)
    if image.any():
        for qr in decode(image):
            text = qr.data.decode("utf-8")
            return text
    else:
        print("Timed Out")


def hash_to_num(string):
    suma = 0
    for letter in string:
        suma += ord(letter)
    return suma % 5
