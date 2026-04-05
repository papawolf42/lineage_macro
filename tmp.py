from PIL import Image
from tools.imageProcesser import image_to_coord_string, crop

img = Image.open("image/screenshot.png")
# s = image_to_coord_string(img, (255, 255, 255))
# print(s)

def crop_show(x, y, w, h):
    cropped = crop(img, x, y, w, h)
    cropped.show()

# 이 좌표의 y축이 
# crop_show(230, 787, 300, 24)
crop_show(230, 787, 300, 24)
