import requests

from cStringIO import StringIO
from PIL import Image

URL = 'http://railway.hinet.net/ImageOut.jsp'
SIZE = (200, 60)

response = requests.get(URL)
stringIO = StringIO(response.content)
image = Image.open(stringIO)
image.save('get.png')

(h, s, v) = image.convert('HSV').split()
h.save('get_h.png')
s.save('get_s.png')
v.save('get_v.png')
