import macro
from tools.imageProcesser import crop

macro.set_hwnd(1117856)
macro.move_window(0, 0)

img = macro.screenshot()
cropped = crop(img, 249, 933, 20, 24)
cropped.save("image/cropped.png")

