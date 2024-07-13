from PIL import Image
import numpy as np

img = Image.open('quirks.png')

pixels = np.array(img).astype(str)

pixels[pixels == '0'] = 'X'
pixels[pixels == '1'] = '_'

s = '\n'.join(''.join(row) for row in pixels)

with open('qr.txt', 'w+') as f:
    f.write(s)