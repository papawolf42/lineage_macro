import json
import time
import macro
import imageProcesser

with open("converted_data.json", "r", encoding="utf-8") as f:
    converted_data = json.load(f)

macro.set_hwnd(1117856)
macro.move_window(0, 0)

time.sleep(3)
img = macro.screenshot()
cropped = imageProcesser.crop(img, 985, 105, 1280-985, 21)
cropped.save("cropped.png")
cropped.show()
