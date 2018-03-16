from mss import mss
from PIL import Image
from time import time
import requests
import httplib2

sct = mss()
initImage = sct.grab(sct.monitors[1])
stripWidth = 100
mon = {'top': 0, 'left': initImage.width - stripWidth, 'width': stripWidth, 'height': initImage.height}


count = 0
img = None
domColor = None

img = Image.new('RGB', (stripWidth, initImage.height))

request = ''
h = httplib2.Http(".cache")

startTime = time()
while True:
    sct_img = sct.grab(mon)
    # Best solution: create a list(tuple(R, G, B), ...) for putdata()
    pixels = zip(sct_img.raw[2::4],
                 sct_img.raw[1::4],
                 sct_img.raw[0::4])

    uniqePixels = set(pixels)
    pixels = list(pixels)
    domColor = max(uniqePixels, key=lambda x: pixels.count(x))

    request = 'http://139.59.206.133/203ed0f06e9244e1ab1b87233c062af3/update/V1?value={}&value={}&value={}'.format(((domColor[0]+1)*4)-1, ((domColor[1]+1)*4)-1, ((domColor[2]+1)*4)-1)

    h.request(request, "GET")
    count = count + 1
    print(count/(time() - startTime))

    if (time() - startTime) > 3:
        startTime = time()
        count = 0