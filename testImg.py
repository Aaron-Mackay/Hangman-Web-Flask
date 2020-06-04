from PIL import Image, ExifTags
import os,sys

print(sys.path.append(os.path.realpath("/static/img/framed_example.png")))

dir = os.getcwd()
print(os.getcwd())
filename = os.path.join(dir, '/static/img/framed_example.png')
print(filename)
img = Image.open(filename)
width, height = im.size