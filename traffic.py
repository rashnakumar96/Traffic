import urllib2, cStringIO, time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
import datetime

def im_from_url(url,proxy):
    proxy = urllib2.ProxyHandler({"http": proxy, "https": proxy})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    data = urllib2.urlopen(url).read()
    # print data
    return Image.open(cStringIO.StringIO(data))

url_template = ("http://mt1.google.com/vt?hl=en&lyrs=m,traffic&" +
                "x=%i&y=%i&z=14&style=15")
               # used to have "h@163315395" instead of "m"

t = 0
x = 11576
y = 6681
w = 3
h = 3

font_file = "Arial Black.ttf"
font = ImageFont.truetype(font_file, 30)

d = 6
t = 0

def traffic(proxy):
    time.sleep(random.randint(0,20))
    out = Image.new('RGB', (256*w,256*h), color=(255,255,255))
    # 'RGBA' for transparency

    for i in range(w):
        for j in range(h):
            im = im_from_url(url_template % (x+i, y+j),proxy)
            im = im.convert('RGBA')
            out.paste(im, (256*i, 256*j), im)

    draw = ImageDraw.Draw(out)
    label = str(datetime.datetime.now())
    (label_w, label_h) = draw.textsize(label, font=font)
    draw.text((0, (256*h-label_h)), label, font=font, fill=(0,0,0))

    out.save(label+".png")