import base64
from io import BytesIO
from PIL import Image

HORIZONTAL  = 0
VERTICAL    = 1

def image_to_base64(img, fmt='png'):
    buffered = BytesIO()
    img.save(buffered, format=fmt)
    img_str = base64.b64encode(buffered.getvalue())
    return img_str

def base64_to_image(img_str):
    img = base64.b64decode(img_str)
    img = BytesIO(img)
    img = Image.open(img)
    return img

def image_concate(imgpth1, imgpth2, outpth=None, direction=HORIZONTAL):
    img1, img2 = Image.open(imgpth1), Image.open(imgpth2)
    siz1, siz2 = img1.size, img2.size
    out = None
    if direction == HORIZONTAL:
        out = Image.new('RGB', (siz1[0]+siz2[0], siz1[1]))
        loc1, loc2 = (0, 0), (siz1[0], 0)
        out.paste(img1, loc1)
        out.paste(img2, loc2)
    elif direction == VERTICAL:
        out = Image.new('RGB', (siz1[0], siz1[1]+siz2[1]))
        loc1, loc2 = (0, 0), (0, siz1[1])
        out.paste(img1, loc1)
        out.paste(img2, loc2)
    if out and outpth:
        out.save(outpth)
    return out